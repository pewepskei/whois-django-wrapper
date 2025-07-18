import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class WhoisLookupAPIView(APIView):
    def get(self, request):
        domain = request.query_params.get('domain')
        info_type = request.query_params.get('info_type', 'all').lower()

        if not domain:
            return Response({
                "error": 'Missing required query parameter: "domain"',
                "accepted_parameters": ["domain", "info_type (optional, values: domain, contact, all)"]
            }, status=status.HTTP_400_BAD_REQUEST)

        if info_type not in ['domain', 'contact', 'all', '']:
            return Response({
                "error": f"Invalid info_type",
                "valid_info_types": ["domain", "contact", "all"]
            }, status=status.HTTP_400_BAD_REQUEST)

        api_key = settings.WHOIS_API_KEY
        if not api_key:
            return Response({'error': 'API key not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        url = "https://www.whoisxmlapi.com/whoisserver/WhoisService"
        params = {
            "apiKey": api_key,
            "domainName": domain,
            "outputFormat": "JSON"
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        except ValueError:
            return Response({'error': 'Invalid response from WHOIS API'}, status=status.HTTP_502_BAD_GATEWAY)

        # Extract necessary fields
        whois_data = data.get("WhoisRecord", {})
        contact_data = whois_data.get("contactEmail") or whois_data.get("registryData", {}).get("contactEmail")

        domain_section = {
            "Domain Name": whois_data.get("domainName"),
            "Registrar": whois_data.get("registrarName"),
            "Registration Date": whois_data.get("createdDate"),
            "Expiration Date": whois_data.get("expiresDate"),
            "Estimated Domain Age": whois_data.get("estimatedDomainAge"),
            "Hostnames": [
                hostname if len(hostname) <= 25 else hostname[:22] + "..."
                for hostname in whois_data.get("hostNames", []) or []
            ]
        }

        contact_section = {
            "Registrant Name": whois_data.get("registrant", {}).get("name"),
            "Technical Contact Name": whois_data.get("technicalContact", {}).get("name"),
            "Administrative Contact Name": whois_data.get("administrativeContact", {}).get("name"),
            "Contact Email": contact_data
        }

        if info_type == "domain":
            return Response({"domain": domain_section})
        elif info_type == "contact":
            return Response({"contact": contact_section})
        else:  # "all"
            return Response({
                "domain": domain_section,
                "contact": contact_section
            })

