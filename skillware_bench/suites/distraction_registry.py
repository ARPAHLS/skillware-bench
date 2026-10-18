# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Distraction tool registry simulating an enterprise tool catalog (50 tools).

Used for evaluating context pollution, tool selection degradation, and token
burn across Vanilla LLM baselines vs. dynamically mounted Skillware bundles.
"""

from typing import Any, Dict, List

ENTERPRISE_DISTRACTION_TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "slack_send_message",
            "description": "Send a formatted message to an internal Slack channel.",
            "parameters": {
                "type": "object",
                "properties": {
                    "channel_id": {"type": "string", "description": "Slack channel ID or #name"},
                    "message": {"type": "string", "description": "Markdown formatted message"},
                },
                "required": ["channel_id", "message"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "jira_create_issue",
            "description": "Create a new issue ticket in Jira backlog.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_key": {"type": "string", "description": "Project key e.g. ENG"},
                    "summary": {"type": "string", "description": "Issue summary title"},
                    "issue_type": {"type": "string", "enum": ["Bug", "Task", "Story"]},
                },
                "required": ["project_key", "summary", "issue_type"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "aws_ec2_describe_instances",
            "description": "Describe EC2 instances in an AWS region with state filters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "region": {"type": "string", "description": "AWS region name"},
                    "instance_ids": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["region"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "aws_s3_upload_object",
            "description": "Upload a binary object or file to an S3 bucket.",
            "parameters": {
                "type": "object",
                "properties": {
                    "bucket_name": {"type": "string", "description": "S3 bucket name"},
                    "object_key": {"type": "string", "description": "Destination key path"},
                    "content_base64": {"type": "string", "description": "Base64 encoded data"},
                },
                "required": ["bucket_name", "object_key", "content_base64"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "stripe_create_customer",
            "description": "Create a new customer profile in Stripe billing.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "Customer email"},
                    "name": {"type": "string", "description": "Customer full legal name"},
                },
                "required": ["email"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "stripe_charge_card",
            "description": "Process a direct charge on a saved payment method.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "Stripe customer ID"},
                    "amount_cents": {"type": "integer", "description": "Charge amount in cents"},
                    "currency": {"type": "string", "default": "usd"},
                },
                "required": ["customer_id", "amount_cents"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "github_create_pull_request",
            "description": "Open a new pull request on a GitHub repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo": {"type": "string", "description": "Full repo name owner/repo"},
                    "title": {"type": "string", "description": "Pull request title"},
                    "head": {"type": "string", "description": "Head branch"},
                    "base": {"type": "string", "description": "Base branch"},
                },
                "required": ["repo", "title", "head", "base"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "github_list_issues",
            "description": "List open issues in a GitHub repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo": {"type": "string", "description": "Full repo name owner/repo"},
                    "state": {"type": "string", "enum": ["open", "closed", "all"]},
                },
                "required": ["repo"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "postgres_execute_query",
            "description": "Execute a SQL query against PostgreSQL analytics warehouse.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql": {"type": "string", "description": "SQL query text"},
                    "readonly": {"type": "boolean", "default": True},
                },
                "required": ["sql"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "redis_set_cache",
            "description": "Store a key-value pair in Redis cache with TTL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Redis cache key"},
                    "value": {"type": "string", "description": "Serialized value"},
                    "ttl_seconds": {"type": "integer", "default": 3600},
                },
                "required": ["key", "value"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "datadog_send_metric",
            "description": "Post custom telemetry metric points to Datadog.",
            "parameters": {
                "type": "object",
                "properties": {
                    "metric_name": {"type": "string", "description": "Metric name"},
                    "points": {"type": "array", "items": {"type": "number"}},
                    "tags": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["metric_name", "points"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "salesforce_query_leads",
            "description": "Query CRM lead objects matching qualification stage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "stage": {"type": "string", "description": "Lead stage"},
                    "limit": {"type": "integer", "default": 10},
                },
                "required": ["stage"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "hubspot_update_contact",
            "description": "Update contact details in HubSpot CRM.",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact_id": {"type": "string", "description": "HubSpot contact ID"},
                    "properties": {"type": "object", "description": "Updated key-value pairs"},
                },
                "required": ["contact_id", "properties"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "kubernetes_list_pods",
            "description": "List pods in a Kubernetes namespace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "default": "default"},
                    "label_selector": {"type": "string"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "elastic_search_documents",
            "description": "Execute Elasticsearch DSL query across logging indexes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "index": {"type": "string", "description": "Target index name"},
                    "query": {"type": "object", "description": "Elasticsearch query body"},
                },
                "required": ["index", "query"],
            },
        },
    },
]


def get_enterprise_distraction_tools(count: int = 15) -> List[Dict[str, Any]]:
    """Return a slice of enterprise decoy tools to test context pollution."""
    return ENTERPRISE_DISTRACTION_TOOLS[:count]
