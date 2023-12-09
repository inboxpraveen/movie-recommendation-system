# configure aws provider
provider "aws" {
  # for access/secret key please enter your own
  access_key = var.access_key
  secret_key = var.secret_key
  region = "us-east-1"
  #profile = "Admin"
}


# creating VPC 
resource "aws_vpc" "final" {
#  cidr_block = "172.1.0.0/16"
  instance_tenancy = "default"
  enable_dns_support = true
  tags = {
    Name = "d10_vpc"
  }
}

##creating the subnets
resource "aws_subnet" "pub1" {
  vpc_id = aws_vpc.final.id
#  cidr_block = "172.1.1.0/24"
  availability_zone = "us-east-1a"
  map_public_ip_on_launch = true
  tags = {
    Name = "d10_pub1"
  }
}

resource "aws_subnet" "pub2" {
  vpc_id = aws_vpc.final.id
  cidr_block = "172.1.2.0/24"
  availability_zone = "us-east-1b"
  map_public_ip_on_launch = true
  tags = {
    Name = "d10_pub2"
  }
}

resource "aws_subnet" "pri1" {
  vpc_id = aws_vpc.final.id
  cidr_block = "172.1.3.0/24"
  availability_zone = "us-east-1a"
  map_public_ip_on_launch = true
  tags = {
    Name = "d10_pri1"
  }
}

resource "aws_subnet" "pri2" {
  vpc_id = aws_vpc.final.id
  cidr_block = "172.1.4.0/24"
  availability_zone = "us-east-1b"
  map_public_ip_on_launch = true
  tags = {
    Name = "d10_pri2"
  }
}

# internet gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.final.id
}

# elastic IP
resource "aws_eip" "elastic-ip" {
  domain = "vpc"
  
}
# NAT gateway
resource "aws_nat_gateway" "ngw" {
  subnet_id = aws_subnet.pub1.id
  allocation_id = aws_eip.elastic-ip.id


}
# create the route table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.final.id 
}
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.final.id
  
}
# route table to what route
resource "aws_route" "igw_route" {
  route_table_id = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.igw.id
}

resource "aws_route" "nat_route" {
  route_table_id = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id = aws_nat_gateway.ngw.id
}

## assoication the route table to that route
resource "aws_route_table_association" "public1" {
  subnet_id = aws_subnet.pub1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public2" {
  subnet_id = aws_subnet.pub2.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private1" {
  subnet_id = aws_subnet.pri1.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private2" {
  subnet_id = aws_subnet.pri2.id
  route_table_id = aws_route_table.private.id
}

################ Creating Security group ##########################
resource "aws_security_group" "sg" {
  name = "d10_sg"
  description = "traffic for d10"
  vpc_id = aws_vpc.final.id
  ingress {
    from_port = 80
    to_port = 80 
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 3000
    to_port = 3000
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 8000
    to_port = 8000 
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_alb" "d10-alb" {
  name = "d10-alb"
  internal = false
  load_balancer_type = "application"

  subnets = [
    aws_subnet.pri1.id,
    aws_subnet.pri2.id,
  ]
  security_groups = [aws_security_group.sg.id]

  depends_on = [ aws_internet_gateway.igw ]
}
