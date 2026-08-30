from services.workflow_registry import WorkflowRegistry, workflow_registry
from luminous.workflows.dailygospelworkflow import DailyGospelWorkflow


def main():

    registry = WorkflowRegistry()

    assert registry.get('Daily Gospel') is DailyGospelWorkflow

    workflow = registry.create('Daily Gospel')

    assert isinstance(
        workflow,
        DailyGospelWorkflow,
    )

    assert 'daily gospel' in registry.names()

    class TestWorkflow:
        pass

    registry.register(
        'Test Workflow',
        TestWorkflow,
    )

    assert registry.get('test workflow') is TestWorkflow

    assert isinstance(
        registry.create('TEST WORKFLOW'),
        TestWorkflow,
    )

    try:
        registry.get('Unknown Workflow')
    except ValueError:
        pass
    else:
        raise AssertionError(
            'Unknown workflow must fail.'
        )

    try:
        registry.register(
            '',
            TestWorkflow,
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            'Empty workflow name must fail.'
        )

    try:
        registry.register(
            'Invalid',
            'not-a-class',
        )
    except TypeError:
        pass
    else:
        raise AssertionError(
            'Invalid workflow class must fail.'
        )

    assert (
        workflow_registry.create('Daily Gospel').__class__
        is DailyGospelWorkflow
    )

    print('=' * 60)
    print('WORKFLOW REGISTRY TEST PASSED')
    print('=' * 60)


if __name__ == '__main__':
    main()
