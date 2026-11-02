# Universal Blind SQLi Extractor

A universal, payload-agnostic blind SQL injection extraction tool.  
The user supplies a payload template with a `{PAYLOAD}` placeholder, and the script handles character probing, request sending, and result extraction.

> ⚠️ **Disclaimer**  
> This tool is intended **for authorized security testing and educational purposes only**.  
> Do not use it against targets without explicit permission.  
> The author is not responsible for any misuse or damage caused by this tool.

---

## Features

- **Payload-agnostic**: user defines the injection logic via `{PAYLOAD}` placeholder.
- **Boolean-based** detection via:
    - response length (`--match length`)
    - HTTP status code (`--match status`)
    - regex (`--match regex`)
    - substring (`--match contains`)
    - **Time-based** detection (`--technique time`) with configurable delay.
    - Supports **GET** and **POST** requests.
    - Custom **cookies** and **headers** for authenticated targets.
    - Configurable **charset** to speed up extraction.
    - No hardcoded DBMS logic — works with MySQL, PostgreSQL, MSSQL, SQLite, Oracle, etc., as long as you provide the right payload.
    
    ---
    
    ## Installation
    
    ```bash
    git clone https://github.com/Roamal/universal-blind-sqli.git
    cd universal-blind-sqli
    pip install -r requirements.txt
