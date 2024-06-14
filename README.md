# sort-dbt-docs
Pre-commit hook that sorts dbt doc blocks in a macro alphabetically.

This pre-commit hook only works if you make use of the docs macro within dbt, since it only iterates over markdown files and ignores yml files. It returns a standardized output of your docs with the format:

```markdown
{% docs aaa %}
Documentation for aaa.
{% enddocs %}

{% docs bbb %}
Documentation for bbb.
{% enddocs %}

```

## Usage
Add this to your `.pre-commit-config.yaml`:
```yml
-   repo: https://github.com/LeopoldGabelmann/sort-dbt-docs.git
    rev: v0.4.0
    hooks:
    -   id: sort-dbt-docs
```

To limit it to your docs folder that most likely sits within your macro folder you can add:
```yml
-   repo: https://github.com/LeopoldGabelmann/sort-dbt-docs.git
    rev: v0.4.0
    hooks:
    -   id: sort-dbt-docs
        files: (^macros/docs/)
```
