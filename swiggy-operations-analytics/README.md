# Food Delivery Operations Analytics

An original, synthetic-data case study for last-mile delivery operations and hub performance.

## Questions addressed
- Which hubs have the highest cancellation rates?
- Which hubs have the weakest on-time delivery performance?
- How do delivery time, estimated cost and customer ratings vary by hub?
- Which hubs should be prioritized for operational root-cause investigation?

## Run
```bash
python -m pip install -r requirements.txt
python src/generate_data.py
python src/analyze_operations.py
```

The data is synthetic and is not actual Swiggy data. This is an independent implementation inspired by public delivery-analytics project ideas. Public references:
- https://github.com/yugandhar1028/Swiggy-Sales-Operations-Analytics-Dashboard
- https://github.com/tiwariprachi657-ops/e-commerce-delivery-analysis
