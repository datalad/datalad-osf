from datalad.tests.utils import assert_result_count


def test_register():
    import datalad.api as da
    assert hasattr(da, 'hello_cmd')
    assert_result_count(
        da.hello_cmd(),
        1,
        action='demo')

