import sys
import os
from datetime import datetime
import instaloader
from instaloader.exceptions import InstaloaderException

def main():
    print("📸 Instagram Image Scraper (Powered by Instaloader)\n")
    
    username = input("Enter Instagram username (without @): ").strip()
    if not username:
        print("❌ Username required!")
        return

    # Configuration
    download_videos = input("Download videos too? (y/n): ").lower() == 'y'
    max_posts = input("Max posts to download (leave empty for all): ").strip()
    max_posts = int(max_posts) if max_posts.isdigit() else None

    folder = f"instagram_{username}_{datetime.now().strftime('%Y%m%d')}"
    
    try:
        L = instaloader.Instaloader(
            dirname_pattern=folder,
            download_pictures=True,
            download_videos=download_videos,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=True,
            compress_json=False,
        )

        print(f"🔍 Loading profile @{username}...")
        profile = instaloader.Profile.from_username(L.context, username)

        print(f"✅ Profile found: {profile.full_name} ({profile.followers} followers)")
        print(f"📊 Total posts: {profile.mediacount}")

        print(f"\n📥 Downloading images to: ./{folder}/")
        
        posts = profile.get_posts()
        count = 0
        
        for post in posts:
            if max_posts and count >= max_posts:
                break
                
            try:
                print(f"Downloading post {count+1} | {post.date} | {'Video' if post.is_video else 'Image'}")
                L.download_post(post, target=username)
                count += 1
            except Exception as e:
                print(f"⚠️  Skipped post: {e}")
                continue

        print(f"\n🎉 Done! Downloaded {count} posts → ./{folder}/")

    except InstaloaderException as e:
        print(f"❌ Instaloader Error: {e}")
        print("💡 Tip: Try logging in for better access (see below)")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Optional: Login for private accounts or higher limits
    if len(sys.argv) > 1 and sys.argv[1] == "--login":
        L = instaloader.Instaloader()
        username = input("Enter your Instagram username: ")
        L.login(username, input("Password: "))
        print("✅ Logged in successfully!")
    
    main()