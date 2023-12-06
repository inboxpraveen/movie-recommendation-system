#################### Configure the AWS provider ####################
provider "aws" {
  region     = "us-east-1"
  access_key = var.access_key
  secret_key = var.secret_key
  # profile = "Admin"
}
#################### Create IAM users ####################
resource "aws_iam_user" "proj_man" {
  name = "projectmanager"
  tags = {
    Role = "Project Manager"
  }
}

resource "aws_iam_user" "chief_arch" {
  name = "architect" 
  tags = {
    Role = "Chief Architect"
  }
}

resource "aws_iam_user" "sys_admin" {
  name = "systemadmin"
  tags = {
    Role = "System Administrator"
  }
}

resource "aws_iam_user" "director" {
  name = "director" 
  tags = {
    Role = "Director"
  }
}

#################### Create access keys for users ####################
resource "aws_iam_access_key" "proj_man" {
  user = aws_iam_user.proj_man.name
}

resource "aws_iam_access_key" "chief_arch" {
  user = aws_iam_user.chief_arch.name
}

resource "aws_iam_access_key" "sys_admin" {
  user = aws_iam_user.sys_admin.name
}

resource "aws_iam_access_key" "director" {
  user = aws_iam_user.director.name
}

#################### Output access and secret keys ####################
output "proj_man_keys" {
  value = {
    access_key_id     = aws_iam_access_key.proj_man.id
    secret_access_key = aws_iam_access_key.proj_man.secret
  }
  sensitive = true
}

output "chief_arch_keys" {
  value = {
    access_key_id = aws_iam_access_key.chief_arch.id
    secret_access_key = aws_iam_access_key.chief_arch.secret
  }
  sensitive = true
}

output "sys_admin_keys" {
  value = {
    access_key_id     = aws_iam_access_key.sys_admin.id
    secret_access_key = aws_iam_access_key.sys_admin.secret
  }
  sensitive = true
}

output "director_keys" {
  value = {
    access_key_id = aws_iam_access_key.director.id
    secret_access_key = aws_iam_access_key.director.secret
  }
  sensitive = true
}

#################### Save access keys locally ####################
locals {
  proj_man_csv = "access_key,secret_key\n${aws_iam_access_key.proj_man.id},${aws_iam_access_key.proj_man.secret}"
  chief_arch_csv = "access_key,secret_key\n${aws_iam_access_key.chief_arch.id},${aws_iam_access_key.chief_arch.secret}"
  sys_admin_csv = "access_key,secret_key\n${aws_iam_access_key.sys_admin.id},${aws_iam_access_key.sys_admin.secret}"
  director_csv = "access_key,secret_key\n${aws_iam_access_key.director.id},${aws_iam_access_key.director.secret}"
}

resource "local_file" "proj_man_keys" {
  filename = "proj-man-keys.csv"
  content  = local.proj_man_csv
}

resource "local_file" "chief_arch_keys" {
  content  = local.chief_arch_csv
  filename = "chief-arch-keys.csv"
}

resource "local_file" "sys_admin_keys" {
  content  = local.sys_admin_csv
  filename = "sys-admin-keys.csv"
}

resource "local_file" "director_keys" {
  content  = local.director_csv
  filename = "director-keys.csv"
}

#################### Create IAM Groups ####################
resource "aws_iam_group" "proj_man" {
  name = "project-manager"
}

resource "aws_iam_group" "chief_arch" {
  name = "chief-architect"
}

resource "aws_iam_group" "sys_admin" {
  name = "sys-admin"
}

resource "aws_iam_group" "director" {
  name = "director"
}

#################### Add users to groups ####################
resource "aws_iam_group_membership" "project_manager" {
  name  = aws_iam_user.proj_man.name
  users = [aws_iam_user.proj_man.name]
  group = aws_iam_group.proj_man.name
}

resource "aws_iam_group_membership" "chief_arch" {
  name = aws_iam_user.chief_arch.name
  users = [aws_iam_user.chief_arch.name]
  group = aws_iam_group.chief_arch.name
}

resource "aws_iam_group_membership" "sys_admin" {
  name  = aws_iam_user.sys_admin.name
  users = [aws_iam_user.sys_admin.name]
  group = aws_iam_group.sys_admin.name
}

resource "aws_iam_group_membership" "director" {
  name = aws_iam_user.director.name
  users = [aws_iam_user.director.name]
  group = aws_iam_group.director.name
}

#################### Custom IAM policy for RDS, ECS, Fargate, EC2 resource access ####################
resource "aws_iam_policy" "resource_access" {
  name        = "group_resource_access"
  description = "Access for group users"

  policy = <<EOF
{
  "Version": "2012-10-17", 
  "Statement": [
    {
      "Action": [
        "rds:*",
        "ecs:*",  
        "ec2:*",
        "elasticloadbalancing:*",
        "autoscaling:*",
        "cloudwatch:*",
        "s3:*",
        "vpc:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

#################### Attach policy to groups ####################
resource "aws_iam_group_policy_attachment" "proj_man_attach" {
  group      = aws_iam_group.proj_man.name
  policy_arn = aws_iam_policy.resource_access.arn
}

resource "aws_iam_group_policy_attachment" "chief_arch_attach" {
  group      = aws_iam_group.chief_arch.name
  policy_arn = aws_iam_policy.resource_access.arn
}

resource "aws_iam_group_policy_attachment" "sys_admin_attach" {
  group      = aws_iam_group.sys_admin.name
  policy_arn = aws_iam_policy.resource_access.arn
}

resource "aws_iam_group_policy_attachment" "director_attach" {
  group      = aws_iam_group.director.name
  policy_arn = aws_iam_policy.resource_access.arn
}

#################### Attach IAM policies for each user ####################
resource "aws_iam_user_policy_attachment" "proj_man_policy" {
  user       = aws_iam_user.proj_man.name
  policy_arn = "arn:aws:iam::aws:policy/job-function/ViewOnlyAccess"
}

resource "aws_iam_user_policy_attachment" "chief_arch_policy" {
  user       = aws_iam_user.chief_arch.name
  policy_arn = "arn:aws:iam::aws:policy/PowerUserAccess"  
}

resource "aws_iam_user_policy_attachment" "sys_admin_policy" {
  user       = aws_iam_user.sys_admin.name
  policy_arn = "arn:aws:iam::aws:policy/job-function/SystemAdministrator"
}

resource "aws_iam_user_policy_attachment" "director_policy" {
  user       = aws_iam_user.director.name
  policy_arn = "arn:aws:iam::aws:policy/ViewOnlyAccess"  
}
