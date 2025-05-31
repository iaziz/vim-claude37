# vim-claude37

A Vim plugin to integrate with Anthropic's Claude 3.7 model via AWS Bedrock, bringing AI-powered assistance directly into your Vim editor.

---

## Features

- Get AI assistance from Claude 3.7 with a simple key mapping
- Natural typing animation for responses
- Configurable model selection via ARN
- Adjustable typing speed
- Works with any AWS Bedrock Claude 3.7 model, including cross-origin inference profiles

---

## Requirements

- Vim 7.0+ compiled with Python 3 support (`+python3`)
- AWS account with access to Bedrock and Claude 3.7
- Python 3 with the `boto3` library installed
- AWS credentials configured (via AWS CLI or environment variables)

---

## Installation

### Using a Plugin Manager (recommended)

**With vim-plug:**
```vim
Plug 'iaziz/vim-claude37'

Then run :PlugInstall

With Vundle:

vim
Plugin 'iaziz/vim-claude37'
Then run :PluginInstall

Manual Installation

Clone the repository:

sh
git clone https://github.com/iaziz/vim-claude37.git ~/.vim/pack/plugins/start/vim-claude37
Make sure you have Python support in Vim:

sh
vim --version | grep +python3
Install required Python packages:

sh
pip install boto3
AWS Setup

IAM Permissions

Ensure your AWS user/role has the appropriate permissions. Here's an example IAM policy:

JSON
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
				"bedrock:InvokeModel",
				"bedrock:InvokeModelWithResponseStream"
			],
			"Resource": [
				"arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-7-sonnet-20250219-v1:0",
				"arn:aws:bedrock:us-east-2::foundation-model/anthropic.claude-3-7-sonnet-20250219-v1:0",
				"arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-7-sonnet-20250219-v1:0"
			]
		},
		{
			"Effect": "Allow",
			"Action": [
				"bedrock:InvokeModel",
				"bedrock:InvokeModelWithResponseStream"
			],
			"Resource": [
				"arn:aws:bedrock:us-east-1:123456789012:inference-profile/*",
				"arn:aws:bedrock:us-east-2:123456789012:inference-profile/*",
				"arn:aws:bedrock:us-west-2:123456789012:inference-profile/*"
			]
		}
	]
}
Note: In the ARN examples above, 123456789012 represents your 12-digit AWS account ID. You'll need to replace this with your actual AWS account ID in your IAM policies and when referencing your inference profile ARNs.

Obtaining a Cross-Origin Inference Profile ARN

To use Claude 3.7, you'll need to create or use a cross-origin inference profile:

Go to the AWS Bedrock console
Navigate to "Model access" in the left sidebar
Ensure Claude 3.7 Sonnet is activated for your account
Go to "Inference profiles" and click "Create inference profile"
Select "Claude 3.7 Sonnet" as the base model
Configure your settings as needed
Create the profile
Once created, copy the ARN, which should look like:
arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0
Where 123456789012 is your actual AWS account ID.
Configuration

Add the following to your .vimrc:

vim
" REQUIRED: Set Claude 3.7 model ARN
let g:claude37_model_arn = 'arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0'

" OPTIONAL: Set typing animation speed (milliseconds per character)
let g:claude37_typing_speed = 5
Be sure to replace 123456789012 with your actual AWS account ID in the model ARN.

AWS Authentication

The plugin uses boto3, which will look for AWS credentials in the standard locations:

Environment variables (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)
Shared credential file (~/.aws/credentials)
AWS config file (~/.aws/config)
IAM role for Amazon EC2 or ECS task role
Make sure your AWS credentials are properly configured before using this plugin.

Usage

Commands

:Claude37Assist - Get assistance from Claude 3.7
:Claude37Clear - Clear the current buffer
Default Mappings

<leader>cg - Trigger Claude 3.7 assistance
Getting Help

With an empty buffer, run :Claude37Assist to start a conversation
With text in your buffer:
If the current line is empty, Claude will analyze the entire buffer content
If the current line has text, Claude will respond to that specific line as a prompt
Troubleshooting

If you encounter issues:

Ensure Vim has Python 3 support: :echo has('python3')
Check your AWS credentials: aws sts get-caller-identity
Verify your IAM permissions for Bedrock
Ensure the model ARN is correctly set in your .vimrc
Make sure the region in boto3.client() matches your model's region
License

MIT License

Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
