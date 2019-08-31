cat main.py | grep -E "import|(from(.)+import)" > test.all_import
cat updater.py | grep -E "import|(from(.)+import)" >> test.all_import