# All the configuration we need is under the folder "serverless"
KEY="serverless"

# Full S3 path
COPY_FROM="s3://$BUCKET/$KEY/"

# Back to root level
cd ..

# Target directory should be the one who contains the serverless.yml
# The scripts works under the assumption we have COPY_TO defined as environment variable
# We then copy everything under the serverless folder in S3 to the targeted directory
aws s3 cp $COPY_FROM $COPY_TO --recursive
