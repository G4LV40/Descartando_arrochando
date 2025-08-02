import boto3
import zipfile
import os
import time

def deploy_to_eb():
    """Deploy usando AWS CLI/SDK"""
    
    # Configurações
    app_name = "classificador-descarte"
    env_name = "classificador-descarte-env"
    region = "us-east-1"
    
    try:
        # Cliente Elastic Beanstalk
        eb_client = boto3.client('elasticbeanstalk', region_name=region)
        s3_client = boto3.client('s3', region_name=region)
        
        # Criar bucket S3 para armazenar código
        bucket_name = f"{app_name}-deploy-{int(time.time())}"
        s3_client.create_bucket(Bucket=bucket_name)
        
        # Upload do ZIP para S3
        s3_client.upload_file('classificador-descarte.zip', bucket_name, 'app.zip')
        
        # Criar aplicação
        try:
            eb_client.create_application(
                ApplicationName=app_name,
                Description='Classificador de objetos para descarte'
            )
        except:
            print("Aplicação já existe")
        
        # Criar versão da aplicação
        version_label = f"v{int(time.time())}"
        eb_client.create_application_version(
            ApplicationName=app_name,
            VersionLabel=version_label,
            SourceBundle={
                'S3Bucket': bucket_name,
                'S3Key': 'app.zip'
            }
        )
        
        # Criar ambiente
        response = eb_client.create_environment(
            ApplicationName=app_name,
            EnvironmentName=env_name,
            SolutionStackName='64bit Amazon Linux 2 v3.4.0 running Python 3.9',
            VersionLabel=version_label,
            OptionSettings=[
                {
                    'Namespace': 'aws:autoscaling:launchconfiguration',
                    'OptionName': 'InstanceType',
                    'Value': 't3.micro'
                }
            ]
        )
        
        print(f"Deploy iniciado!")
        print(f"URL será: {response['CNAME']}")
        print("Aguarde 5-10 minutos para conclusão")
        
    except Exception as e:
        print(f"Erro: {e}")
        print("Certifique-se de ter AWS CLI configurado:")
        print("aws configure")

if __name__ == "__main__":
    deploy_to_eb()