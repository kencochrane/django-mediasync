from mediasync.backends.s3 import Client as S3Client
from mediasync.conf import msettings

class Client(S3Client):
    """
        Since CloudFront is just a wrapper around S3 we can extend S3 and override a few of the
        minor things that are different. Most notibily the domain name.
        
        #TODO features to add in future
            * Ability to invalidate files in cloudfront
            * support for streaming?
    """
    
    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
        
        self.cloudfront_domain_name = msettings['CLOUDFRONT_DOMAIN_NAME']
        self.aws_prefix = msettings.get('AWS_PREFIX', '').strip('/')
        
        
    def remote_media_url(self, with_ssl=False):
        """
        Returns the base remote media URL. In this case, we can safely make
        some assumptions on the URL string based on bucket names, and having
        public ACL on.
        
        args:
          with_ssl: (bool) If True, return an HTTPS url.
        """
        protocol = 'http' if with_ssl is False else 'https'
        url = ("%s://%s" % (protocol, self.cloudfront_domain_name))
        if self.aws_prefix:
            url = "%s/%s" % (url, self.aws_prefix)
        return url