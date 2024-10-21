import os
from datetime import datetime

def generate_index():
    scp_dir = "entries"
    index_file = os.path.join(scp_dir, "index.html")
    entries = [f for f in os.listdir(scp_dir) if f.endswith(".html") and f != "index.html"]
    entry_names = [f.replace(".html", "") for f in entries]

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SCP Foundation - Secure, Contain, Protect</title>
        <style>
            body {{
                font-family: 'Courier New', monospace;
                line-height: 1.6;
                padding: 20px;
                background-color: #f0f0f0;
                color: #333;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #990000;
                text-align: center;
                border-bottom: 2px solid #990000;
                padding-bottom: 10px;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin-bottom: 10px;
                padding: 10px;
                background-color: #f9f9f9;
                border-left: 3px solid #990000;
            }}
            a {{
                color: #990000;
                text-decoration: none;
                font-weight: bold;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .update-info {{
                text-align: right;
                font-style: italic;
                margin-top: 20px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>SCP Foundation Archives</h1>
            <ul>
                {''.join(f'<li><a href="{entry}">{entry_name}</a></li>' for entry_name, entry in sorted(zip(entry_names, entries), key=lambda x: x[0]))}
            </ul>
            <p class="update-info">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </body>
    </html>
    """

    with open(index_file, "w") as f:
        f.write(html_content)

    print(f"Index file updated: {index_file}")

if __name__ == "__main__":
    generate_index()

