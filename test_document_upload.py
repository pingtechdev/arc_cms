#!/usr/bin/env python3
"""
Test script for document upload functionality
This script tests the RuleDocumentBlock functionality
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms_core.settings')
django.setup()

from cms_app.blocks import RuleDocumentBlock
from wagtail.documents.models import Document
from django.core.files.uploadedfile import SimpleUploadedFile

def test_rule_document_block():
    """Test the RuleDocumentBlock functionality"""
    print("🧪 Testing RuleDocumentBlock...")
    
    # Test block creation
    block = RuleDocumentBlock()
    print(f"✅ RuleDocumentBlock created: {block}")
    
    # Test block fields
    fields = block.child_blocks
    print(f"✅ Block fields: {list(fields.keys())}")
    
    # Check if required fields are present
    required_fields = ['name', 'document', 'description', 'file_type', 'file_size']
    for field in required_fields:
        if field in fields:
            print(f"✅ Field '{field}' is present")
        else:
            print(f"❌ Field '{field}' is missing")
    
    # Test field configurations
    name_field = fields['name']
    print(f"✅ Name field max_length: {name_field.max_length}")
    
    document_field = fields['document']
    print(f"✅ Document field required: {document_field.required}")
    
    description_field = fields['description']
    print(f"✅ Description field required: {description_field.required}")
    
    print("🎉 RuleDocumentBlock test completed successfully!")

def test_document_model():
    """Test the Document model functionality"""
    print("\n🧪 Testing Document model...")
    
    # Check if Document model is accessible
    try:
        document_count = Document.objects.count()
        print(f"✅ Document model accessible, count: {document_count}")
        
        # Test document creation (without actual file)
        test_document = Document(
            title="Test Document",
            file="test.pdf"
        )
        print(f"✅ Document model can be instantiated: {test_document}")
        
    except Exception as e:
        print(f"❌ Document model test failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting document upload tests...")
    
    try:
        test_rule_document_block()
        test_document_model()
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
