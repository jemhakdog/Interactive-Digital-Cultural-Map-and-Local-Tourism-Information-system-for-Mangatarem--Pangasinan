import logging
from utils.db_manager import get_database_uri
from dotenv import load_dotenv

# Configure logging to see the output
logging.basicConfig(level=logging.INFO)


def verify_integration():
    load_dotenv()
    print("\n🔍 VERIFYING DB MANAGER INTEGRATION...")
    try:
        uri = get_database_uri()
        # Mask password for security in output
        if "@" in uri:
            prefix, suffix = uri.split("@")
            masked_prefix = prefix.split(":")[0] + "://...:****"
            print(f"✅ Successfully constructed URI: {masked_prefix}@{suffix}")
        else:
            print(f"✅ Connection URI style: {uri}")

    except Exception as e:
        print(f"❌ Verification failed: {e}")


if __name__ == "__main__":
    verify_integration()
