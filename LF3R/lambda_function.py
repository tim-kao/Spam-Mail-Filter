import boto3, os, datetime


def lambda_handler(event, context):
    endpoint_name = os.environ['endpoint_name']

    training_job_name = os.environ['training_job_name']
    model_role = os.environ['MODEL_ROLE']
    sm = boto3.client('sagemaker')
    job = sm.describe_training_job(TrainingJobName=training_job_name)

    training_job_prefix = os.environ['training_job_prefix']
    training_job_name = training_job_prefix + \
                        str(datetime.datetime.today()).replace(' ', '-').replace(':', '-').rsplit('.')[0]
    job['ResourceConfig']['InstanceType'] = os.environ['instance_type']
    job['ResourceConfig']['InstanceCount'] = int(os.environ['instance_count'])

    # print("Starting training job %s" % training_job_name)

    if 'VpcConfig' in job:
        resp = sm.create_training_job(
            TrainingJobName=training_job_name, AlgorithmSpecification=job['AlgorithmSpecification'],
            RoleArn=job['RoleArn'],
            InputDataConfig=job['InputDataConfig'], OutputDataConfig=job['OutputDataConfig'],
            ResourceConfig=job['ResourceConfig'], StoppingCondition=job['StoppingCondition'],
            HyperParameters=job['HyperParameters'] if 'HyperParameters' in job else {},
            VpcConfig=job['VpcConfig'],
            Tags=job['Tags'] if 'Tags' in job else [])
    else:
        # Because VpcConfig cannot be empty like HyperParameters or Tags :-/
        resp = sm.create_training_job(
            TrainingJobName=training_job_name, AlgorithmSpecification=job['AlgorithmSpecification'],
            RoleArn=job['RoleArn'],
            InputDataConfig=job['InputDataConfig'], OutputDataConfig=job['OutputDataConfig'],
            ResourceConfig=job['ResourceConfig'], StoppingCondition=job['StoppingCondition'],
            HyperParameters=job['HyperParameters'] if 'HyperParameters' in job else {},
            Tags=job['Tags'] if 'Tags' in job else [])

    # print(resp)

    # Waiting for job to finish training
    sm.get_waiter('training_job_completed_or_stopped').wait(TrainingJobName=training_job_name);

    new_job = sm.describe_training_job(TrainingJobName=training_job_name)

    print(new_job)

    # Creating Model
    model_data = new_job['ModelArtifacts']['S3ModelArtifacts']
    primary_container = {
        'Image': new_job['AlgorithmSpecification']['TrainingImage'],
        'ModelDataUrl': model_data
    }
    print(model_data)
    model_name = training_job_name + "-model";
    model_arn = sm.create_model(
        ModelName=model_name,
        ExecutionRoleArn=new_job['RoleArn'],
        PrimaryContainer=primary_container
    )

    # Creating Endpoint Configuration
    epc_name = training_job_name + "-epc"
    ep_config = sm.create_endpoint_config(EndpointConfigName=epc_name, ProductionVariants=[
        {'InstanceType': job['ResourceConfig']['InstanceType'],
         'InitialInstanceCount': job['ResourceConfig']['InstanceCount'], 'ModelName': model_name,
         'VariantName': 'main'}])

    print(ep_config)
    # Updating Endpoint
    sm.update_endpoint(EndpointName=endpoint_name, EndpointConfigName=epc_name)

    print('Training and update succeed')
