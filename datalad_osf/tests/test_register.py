from datalad.tests.utils import assert_result_count


def test_register():
    import datalad.api as da
    assert hasattr(da, 'osf_cmd')
    assert_result_count(
        da.osf_cmd(),
        1,
        action='demo')

