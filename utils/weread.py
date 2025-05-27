
import base64
import os
import httpx

async def get_access_token(code):
        """获取 Notion access token"""
        try:
            print(os.getenv("NOTION_CLIENT_ID"))
            print(os.getenv("NOTION_CLIENT_SECRET"))
            # 用base64编码
            # const encoded = Buffer.from(`${clientId}:${clientSecret}`).toString("base64");
            encoded = base64.b64encode(f"{os.getenv('NOTION_CLIENT_ID')}:{os.getenv('NOTION_CLIENT_SECRET')}".encode()).decode()
            headers = {
                "Authorization": f"Basic {encoded}"
            }
            q_json = {
                "grant_type": "authorization_code",
                "code":  code,
                "redirect_uri": "https://api.dggpt.top/api/get_token",
            }
            async with httpx.AsyncClient() as client:
                response = await client.post("https://api.notion.com/v1/oauth/token", json=q_json, headers=headers)
                response_data = response.json()
                print(response_data)
                access_token = response_data.get("access_token", "")
                if not access_token:
                    raise Exception("Failed to get access token")
                return access_token
                
        except Exception as e:
           raise Exception(f"Error getting access token: {str(e)}")

async def get_page_id(access_token):
    """获取 Notion page ID"""
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.notion.com/v1/search", headers=headers, json={})
            response_data = response.json()
            # 假设我们取第一个页面的 ID
            results = response_data.get("results", [])
            if results:
                page_id = results[0].get("id", "")
                return page_id
            if not page_id:
                raise Exception("No pages found")
    except Exception as e:
        raise Exception(f"Error getting page ID: {str(e)}")
    

if __name__ == "__main__":
    access_token = "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"
    print(access_token)
    import asyncio
    print(asyncio.run(get_page_id(access_token)))
    # page_id = get_page_id(access_token)
    # print(page_id)
