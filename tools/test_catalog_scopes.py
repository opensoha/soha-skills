import copy
import unittest

from validate_assets import ValidationError, load_capability_catalog, validate_gateway_catalog_tool_record


class CatalogScopesTest(unittest.TestCase):
    def test_only_permission_checked_global_template_reads_can_omit_scope(self):
        tools = {tool["name"]: tool for tool in load_capability_catalog()["tools"]}
        record = copy.deepcopy(tools["delivery.deployment_templates.list"])
        validate_gateway_catalog_tool_record(record, set(), set())
        for change in ({"name": "delivery.applications.detail"}, {"riskLevel": "mutate"}, {"permissionKeys": []}):
            with self.subTest(change=change), self.assertRaises(ValidationError):
                validate_gateway_catalog_tool_record({**record, **change}, set(), set())


if __name__ == "__main__":
    unittest.main()
