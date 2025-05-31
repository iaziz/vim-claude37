import vim
import boto3
import json
from botocore.exceptions import ClientError

# Initialize the Bedrock client
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def check_model_arn():
    """Check if model ARN is configured and exists in Vim context"""
    if not vim.eval("exists('g:claude37_model_arn')") == '1':
        vim.command("echoerr 'Error: g:claude37_model_arn is not set. Please set it in your .vimrc file'")
        return False
    
    model_arn = vim.eval('g:claude37_model_arn').strip()
    if not model_arn:
        vim.command("echoerr 'Error: g:claude37_model_arn is empty. Please set a valid ARN in your .vimrc file'")
        return False
    
    return True

def get_claude37_response(prompt, max_retries=5, initial_backoff=1):
    """Get a response from Claude 3.7 via AWS Bedrock"""
    if not prompt.strip():
        return "Error: Empty prompt. Please provide some text."

    # Check if model ARN is properly configured
    if not check_model_arn():
        return "Error: Model ARN not configured. Please set g:claude37_model_arn in your .vimrc file."

    # Get model ARN from vim configuration
    model_arn = vim.eval('g:claude37_model_arn')

    for attempt in range(max_retries):
        try:
            response = bedrock.invoke_model(
                modelId=model_arn,
                contentType='application/json',
                accept='application/json',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 1,
                    "top_p": 0.999,
                })
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
        except ClientError as e:
            if e.response['Error']['Code'] == 'ThrottlingException':
                if attempt < max_retries - 1:
                    wait_time = initial_backoff * (2 ** attempt)
                    vim.command(f"echo 'Rate limited. Retrying in {wait_time} seconds...'")
                    vim.command(f"sleep {wait_time}")
                else:
                    return "Error: Rate limit exceeded. Please try again later."
            else:
                return f"Error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

def clear_buffer():
    """Clear the current buffer"""
    del vim.current.buffer[:]
    vim.command("echo 'Buffer cleared'")

def vim_claude37_assist():
    """Handle the Claude37Assist command"""
    # First check if model ARN is configured
    if not check_model_arn():
        return
        
    current_line = vim.current.line.strip()
    buffer_content = "\n".join(vim.current.buffer).strip()

    if not buffer_content:
        prompt = "Hello!"
    elif not current_line:
        prompt = f"Here's the content of my current buffer. Please provide insights or suggestions:\n\n{buffer_content}"
    else:
        prompt = current_line

    # Show a message while waiting for API response
    vim.command("echo 'Requesting response from Claude 3.7...'")
    
    # Get response from Claude
    response = get_claude37_response(prompt)
    vim.command("echo ''")  # Clear the message
    
    # Properly escape the response for Vim command
    escaped_response = response.replace("'", "''").replace('\\', '\\\\').replace('\n', '\\n')
    
    if not buffer_content:
        # For empty buffer, create human prompt and response
        escaped_prompt = prompt.replace("'", "''").replace('\\', '\\\\').replace('\n', '\\n')
        vim.current.buffer[:] = [""]  # Start with empty line
        vim.command("py3 animated_typing('Human: " + escaped_prompt + "\\n')")
        vim.command("py3 animated_typing('Assistant: " + escaped_response + "')")
    else:
        # Insert response at current position
        vim.command("py3 animated_typing('" + " \\n\\n" + escaped_response + "')")

    vim.command("redraw")
