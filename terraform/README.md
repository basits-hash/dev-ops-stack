# Terraform Infrastructure Configuration

This directory contains Infrastructure as Code (IaC) using Terraform to deploy the Task Manager application to AWS.

## Architecture

The infrastructure includes:

- **VPC**: Custom VPC with public subnets across multiple availability zones
- **ECS Cluster**: Fargate-based container orchestration
- **Application Load Balancer**: Distributes traffic across containers
- **CloudWatch**: Logging and monitoring
- **Security Groups**: Network security configuration

## Prerequisites

1. AWS Account with appropriate permissions
2. Terraform >= 1.0 installed
3. AWS CLI configured with credentials

## Configuration

### Backend Configuration

Update the S3 backend configuration in `main.tf`:

```hcl
backend "s3" {
  bucket = "your-terraform-state-bucket"
  key    = "terraform.tfstate"
  region = "us-east-1"
}
```

### Variables

Create a `terraform.tfvars` file:

```hcl
aws_region   = "us-east-1"
project_name = "task-manager"
environment  = "production"
vpc_cidr     = "10.0.0.0/16"
app_count    = 2
```

## Usage

### Initialize Terraform

```bash
terraform init
```

### Plan Infrastructure Changes

```bash
terraform plan
```

### Apply Infrastructure

```bash
terraform apply
```

### Destroy Infrastructure

```bash
terraform destroy
```

## Outputs

After applying, Terraform will output:

- `alb_dns_name`: Load balancer DNS for accessing the application
- `ecs_cluster_name`: Name of the ECS cluster
- `vpc_id`: VPC identifier
- `cloudwatch_log_group`: CloudWatch log group name

## Cost Optimization

- Use Fargate Spot for non-production workloads
- Implement auto-scaling policies
- Use appropriate instance sizes
- Set up CloudWatch alarms for cost monitoring

## Security Best Practices

1. Store state file in encrypted S3 bucket
2. Use IAM roles with least privilege
3. Enable VPC Flow Logs
4. Implement AWS WAF for ALB
5. Rotate credentials regularly
6. Enable MFA for AWS account

## Monitoring

CloudWatch metrics are automatically collected for:
- ECS task CPU/Memory utilization
- ALB request count and latency
- Target health checks

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure AWS credentials have necessary permissions
2. **State Lock**: If state is locked, check for running Terraform processes
3. **Resource Limits**: Check AWS service quotas for your region

## Additional Resources

- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
