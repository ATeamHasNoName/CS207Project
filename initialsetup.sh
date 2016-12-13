sudo apt-get update
wget http://s3.amazonaws.com/cs207-bucket/cs207_aws_ec2_stack.sh
wget http://s3.amazonaws.com/cs207-bucket/cs207_aws_ec2_stack_test.py
wget http://s3.amazonaws.com/cs207-bucket/cs207_aws_ec2_postgres_test.py
mv cs207_aws_ec2_stack.sh ../cs207_aws_ec2_stack.sh
mv cs207_aws_ec2_stack_test.py ../cs207_aws_ec2_stack_test.py
mv cs207_aws_ec2_postgres_test.py ../cs207_aws_ec2_postgres_test.py
cd ..
chmod a+x cs207_aws_ec2_stack.sh
sudo ./cs207_aws_ec2_stack.sh
