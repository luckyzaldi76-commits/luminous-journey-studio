import tempfile
from pathlib import Path

from engine.production_engine import ProductionEngine
from services.workflow_registry import workflow_registry


def main():

    assert 'daily gospel' in workflow_registry.names()

    with tempfile.TemporaryDirectory() as temp:

        output_dir = Path(temp)

        engine = ProductionEngine()

        result = engine.run(
            gospel='Matius 24:42-51',
            language='ID',
            audience='adult',
            output_dir=output_dir,
            workflow_name='Daily Gospel',
        )

        assert isinstance(result, dict)

        assert result['gospel'] == 'Matius 24:42-51'
        assert result['language'] == 'ID'
        assert result['audience'] == 'adult'

        files = list(output_dir.rglob('*'))

        assert files, 'Workflow produced no output.'

    print('=' * 60)
    print('WORKFLOW RUNTIME INTEGRATION TEST PASSED')
    print('=' * 60)


if __name__ == '__main__':
    main()
