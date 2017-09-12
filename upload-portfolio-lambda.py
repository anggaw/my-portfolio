import boto3
import StringIO
import zipfile
import mimetypes



def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    sns = boto3.resource('sns')

    try:
        topic = sns.Topic('arn:aws:sns:ap-southeast-1:458562924063:deployportfolio')
        portfolio_bucket = s3.Bucket('portfolio.anggawibisono')
        build_bucket = s3.Bucket('portfoliobuild.anggawibisono')

        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('portfoliobuild.zip',portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm,
                    ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        print "Job Done!"
        topic.publish(Subject="Portfolio Deployed", Message="Portfolio Deployed Successfully")
    except:
        topic.publish(Subject="Portfolio Deployed", Message="Portfolio Deployed Failed")
        raise
    return 'Hello from Lambda'
