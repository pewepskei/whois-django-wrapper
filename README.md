# 🔍 Whois Lookup Django Wrapper

A lightweight Django REST API that wraps the **WhoisXML API**, making it easy to fetch WHOIS data for any domain.

---

## ✅ Requirements

- **Python ≥ 3.8**

---

## 📦 Quick Start

1. **Clone the repo**

   ```bash
   git clone https://github.com/pewepskei/whois‑lookup‑django‑wrapper.git
   cd whois‑lookup‑django‑wrapper
   ```

2. **Create & activate a virtual env**

   ```bash
   python3 -m venv env
   source env/bin/activate              # Windows: env\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key**

   Modify the `.env` file in the project root:

   ```
   WHOIS_API_KEY=your_api_key_here
   ```

   Grab a key from <https://user.whoisxmlapi.com/products>.

5. **Run the dev server**

   ```bash
   python3 manage.py runserver 0.0.0.0:8000
   ```

---

## 🌐 Endpoint

| Method | Path                    | Description                    |
|--------|-------------------------|--------------------------------|
| GET    | `/api/whois-lookup`    | Query WHOIS data for a domain. |

### Query Parameters

| Name        | Required | Accepted Values                | Default | Notes                                    |
|-------------|----------|--------------------------------|---------|------------------------------------------|
| `domain`    | ✅       | A fully‑qualified domain name  | —       | e.g. `example.com`                       |
| `info_type` | ❌       | `domain`, `contact`, `all`     | `all`   | Filters the JSON response                |

---

## 🔧 Response Shapes

### `info_type=domain`

```json
{
  "domain": {
    "Domain Name":           "example.com",
    "Registrar":             "Example Registrar, Inc.",
    "Registration Date":     "2010-01-01T00:00:00Z",
    "Expiration Date":       "2030-01-01T00:00:00Z",
    "Estimated Domain Age":  "100", // in days
    "Hostnames": [
      "ns1.example.com",
      "very‑long‑hostname‑example...."
    ]
  }
}
```

### `info_type=contact`

```json
{
  "contact": {
    "Registrant Name":            "John Doe",
    "Technical Contact Name":     "Jane Tech",
    "Administrative Contact Name":"Admin Example",
    "Contact Email":              "admin@example.com"
  }
}
```

### `info_type=all` (or omitted)

```json
{
  "domain": { ... },
  "contact": { ... }
}
```

---

## 🚀 Live Demo

Try it out:

```
https://whois.pewepskei.dev/api/whois-lookup?domain=google.com
```
