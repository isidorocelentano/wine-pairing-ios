"""
Consistency check for regional pairings
Ensures wine descriptions match the country/region context
"""
import asyncio
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ.get('MONGO_URL')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]


async def check_consistency():
    """Check all pairings for logical consistency"""
    
    print("🔍 Consistency Check for Regional Pairings\n")
    print("=" * 80)
    
    issues = []
    
    # Get all pairings
    pairings = await db.regional_pairings.find({}, {"_id": 0}).to_list(100)
    
    print(f"\n📊 Checking {len(pairings)} pairings...\n")
    
    for pairing in pairings:
        country = pairing.get('country', '')
        region = pairing.get('region', '')
        dish = pairing.get('dish', '')
        wine_name = pairing.get('wine_name', '')
        wine_desc = pairing.get('wine_description', '')
        wine_desc_en = pairing.get('wine_description_en', '')
        
        # Check for mismatches
        issue_found = False
        issue_details = []
        
        # French dishes should have French wines (mostly)
        if country == "Frankreich":
            if "Schweiz" in wine_desc or "Swiss" in wine_desc_en:
                issue_found = True
                issue_details.append("❌ French dish with Swiss wine description")
            if "österreich" in wine_desc.lower() or "austrian" in wine_desc_en.lower():
                issue_found = True
                issue_details.append("❌ French dish with Austrian wine description")
        
        # Burgundy context
        if "Burgund" in wine_name or "Burgundy" in wine_name:
            if "Schweiz" in wine_desc or "Swiss" in wine_desc_en:
                issue_found = True
                issue_details.append("❌ Burgundy wine with Swiss description")
            if "Graubünden" in wine_desc or "Graubünden" in wine_desc_en:
                issue_found = True
                issue_details.append("❌ Burgundy wine mentions Graubünden")
        
        # Swiss dishes should have Swiss wines (mostly)
        if country == "Schweiz":
            if "Burgund" in wine_desc and "Schweiz" not in wine_desc:
                issue_found = True
                issue_details.append("❌ Swiss dish with Burgundy-only description")
        
        # Riesling checks
        if "Riesling" in wine_name:
            if country == "Deutschland" and "Elsass" in wine_desc and "deutsch" not in wine_desc.lower():
                issue_found = True
                issue_details.append("❌ German dish with Alsatian Riesling description")
            if country == "Frankreich" and "deutsch" in wine_desc.lower() and "Elsass" not in wine_desc:
                issue_found = True
                issue_details.append("❌ French dish with German Riesling description")
        
        if issue_found:
            issues.append({
                'country': country,
                'region': region,
                'dish': dish,
                'wine_name': wine_name,
                'problems': issue_details,
                'wine_desc_snippet': wine_desc[:80] + "..." if wine_desc else "N/A"
            })
    
    # Report issues
    if issues:
        print(f"⚠️  Found {len(issues)} consistency issues:\n")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue['country']} - {issue['region']}")
            print(f"   Dish: {issue['dish']}")
            print(f"   Wine: {issue['wine_name']}")
            for problem in issue['problems']:
                print(f"   {problem}")
            print(f"   Current desc: {issue['wine_desc_snippet']}")
            print()
    else:
        print("✅ No consistency issues found!")
    
    return issues


async def main():
    issues = await check_consistency()
    
    if issues:
        print("=" * 80)
        print(f"\n🔧 Need to fix {len(issues)} issues")
        print("\nProblematic pairings:")
        for issue in issues:
            print(f"  - {issue['country']}: {issue['dish']} + {issue['wine_name']}")
    else:
        print("\n" + "=" * 80)
        print("✅ All pairings are consistent!")


if __name__ == '__main__':
    asyncio.run(main())
