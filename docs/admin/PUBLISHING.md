# Publishing to PyPI

1. cd to top level project and build dist packages.
    ```
    python setup.py sdist bdist_wheel
    ```

1. Upload to test PyPI.
    ```
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    ```

1. Create local env and test package uploaded as expected.
    ```
    pip install --index-url https://test.pypi.org/simple/ --no-deps edatk
    ```

1. Upload to prod PyPI.
    ```
    twine upload dist/*
    ```

1. Test prod upload ensuring no issues.
    ```
    pip install edatk
    ```
