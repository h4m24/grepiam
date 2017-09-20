## CLI utility to find ec2 instances machine on aws IAM role 

### script will write name/suffix based on Name Tag to a file called variables.json

example:
```
python3 profile-gen.py -n jenkins-production-fra
Found the the Name and the IAM role name, writing the following to file .. ./variables.json
{
    "id": "jenkins-production-fra",
    "machine_iam_role": "jenkins-iam-role"
}
```
### script is readonly there is 0 chance to result in changes on aws account