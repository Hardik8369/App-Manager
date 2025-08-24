from django.shortcuts import render, redirect
from .utils import scan_for_duplicates, load_config  # Make sure both are in utils.py
import os
import json

# Tab options for frontend navigation
TABS = ['Scanner', 'Duplicates']

def home(request):
    config = load_config()
    selected_tab = request.GET.get('tab', 'Scanner').capitalize()

    context = {
        "stats": {
            "Total Files": 32,        # You can update these dynamically if needed
            "Duplicates": 8,
            "Categories": 3,
            "Unique": 24,
            "Scanned": 4,
            "Moved": 3
        },
        "directories": [{"label": d, "value": d} for d in config.get("scan_directories", [])],
        "tabs": TABS,
        "active_tab": selected_tab,
        "duplicates": request.session.get("duplicates", []) if selected_tab == "Duplicates" else [],
    }

    return render(request, 'deduplicator/index.html', context)

def scan_directories(request):
    if request.method == "POST":
        paths = request.POST.getlist("directories")
        custom = request.POST.get("custom_directory")

        if custom:
            paths.append(custom)

        # Update config
        config = load_config()
        config['scan_directories'] = list(set(config.get('scan_directories', []) + paths))
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

        # Run scan
        result = scan_for_duplicates(paths)
        request.session["duplicates"] = result['duplicates']

    return redirect('/')
