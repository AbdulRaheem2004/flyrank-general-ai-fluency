#!/usr/bin/env python3
"""
Model Context Protocol (MCP) Reference Server — stdio JSON-RPC 2.0
Exposes Tools, Resources, and Prompts according to the MCP 2024-11-05 specification.
"""
import os
import sys
import json
import time

def handle_request(req):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})
    
    # 1. Handshake: Initialize
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "flyrank-mcp-server",
                    "version": "1.0.0"
                },
                "capabilities": {
                    "tools": {"listChanged": False},
                    "resources": {"subscribe": False, "listChanged": False},
                    "prompts": {"listChanged": False}
                }
            }
        }
    
    # 2. List Tools
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "write_file",
                        "description": "Write or overwrite content to a local file on host block storage.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string"},
                                "content": {"type": "string"}
                            },
                            "required": ["path", "content"]
                        }
                    },
                    {
                        "name": "get_file_info",
                        "description": "Retrieve physical OS inode metadata (size, permissions, timestamps).",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string"}
                            },
                            "required": ["path"]
                        }
                    },
                    {
                        "name": "read_file",
                        "description": "Read file content from local disk storage.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string"}
                            },
                            "required": ["path"]
                        }
                    }
                ]
            }
        }
    
    # 3. Call Tool
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "write_file":
            path = args.get("path")
            content = args.get("content", "")
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            size = os.path.getsize(path)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Successfully wrote {size} bytes to {path}"
                        }
                    ],
                    "isError": False
                }
            }
            
        elif tool_name == "get_file_info":
            path = args.get("path")
            if not os.path.exists(path):
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Error: File not found at {path}"}],
                        "isError": True
                    }
                }
            stat = os.stat(path)
            info = {
                "path": path,
                "size_bytes": stat.st_size,
                "isFile": os.path.isfile(path),
                "isDirectory": os.path.isdir(path),
                "permissions_octal": oct(stat.st_mode)[-3:],
                "created_time": time.ctime(stat.st_ctime),
                "modified_time": time.ctime(stat.st_mtime)
            }
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(info, indent=2)
                        }
                    ],
                    "isError": False
                }
            }
            
        elif tool_name == "read_file":
            path = args.get("path")
            if not os.path.exists(path):
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Error: File not found at {path}"}],
                        "isError": True
                    }
                }
            with open(path, "r", encoding="utf-8") as f:
                data = f.read()
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": data}],
                    "isError": False
                }
            }
            
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
            }
            
    # 4. List Resources
    elif method == "resources/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "resources": [
                    {
                        "uri": "resource://syllabus/cs701",
                        "name": "CS701 Machine Learning Course Policy",
                        "description": "Official course late submission rules and grading rubric",
                        "mimeType": "text/markdown"
                    }
                ]
            }
        }
        
    # 5. Read Resource
    elif method == "resources/read":
        uri = params.get("uri")
        if uri == "resource://syllabus/cs701":
            policy_doc = (
                "# CS701 Course Policy: Extensions & Late Work\n"
                "- Standard penalty: 10% per 24 hours late.\n"
                "- Emergency extensions: Permitted up to 3 days with documented notice.\n"
                "- Office hours: Mon/Wed 14:00-16:00 (Dr. Ahmed, CS-304)."
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": "text/markdown",
                            "text": policy_doc
                        }
                    ]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": f"Resource URI not found: {uri}"}
            }
            
    # 6. List Prompts
    elif method == "prompts/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "prompts": [
                    {
                        "name": "draft_extension_request",
                        "description": "Standardized prompt template for requesting assignment extensions.",
                        "arguments": [
                            {"name": "professor_name", "description": "Name of professor", "required": True},
                            {"name": "assignment_name", "description": "Name of assignment", "required": True},
                            {"name": "reason", "description": "Reason for extension", "required": True}
                        ]
                    }
                ]
            }
        }
        
    # 7. Get Prompt
    elif method == "prompts/get":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "draft_extension_request":
            prof = args.get("professor_name", "[Professor Name]")
            asg = args.get("assignment_name", "[Assignment Name]")
            rsn = args.get("reason", "[Reason]")
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "description": "Generated Extension Request Prompt Template",
                    "messages": [
                        {
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": f"Draft a concise, professional email to {prof} requesting a 2-day extension on {asg} due to {rsn}. Strictly adhere to the course late policy."
                            }
                        }
                    ]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Unknown prompt: {name}"}
            }
            
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method not supported: {method}"}
        }

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
