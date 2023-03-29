"""Board list page."""
from nicegui import ui

from hermes.core.config import settings
from hermes.gui import AbstractPage, pages


@pages.page(path='/boards', title='My boards')  # type: ignore
class BoardListPage(AbstractPage):
    """Board list page."""
    filter = ''

    def content(self) -> None:  # noqa: D102

        boards = settings.get(['boards'])

        with ui.table(columns=[
            {'name': 'status', 'label': 'Status', 'field': 'status', 'align': 'center', 'style': 'width: 120px'},
            {'name': 'name', 'label': 'Name', 'field': 'name', 'align': 'left', 'sortable': True,
             'style': 'width: 55%'},
            {'name': 'type', 'label': 'Type', 'field': 'type', 'align': 'left', 'sortable': True,
             'style': 'width: 20%'},
            {'name': 'protocol', 'label': 'Protocol', 'field': 'protocol', 'align': 'left', 'sortable': True,
             'style': 'width: 25%'},
            {'name': 'actions', 'label': 'Actions', 'field': 'actions', 'align': 'left', 'style': 'width: 120px'},
        ], rows=[{
            'id': board.id,
            'status': board.connected,
            'name': board.name,
            'type': board.controller + ' ' + board.model,
            'protocol': board.protocol.name,
            'actions': ['edit', 'delete'],
        } for board in boards.values()], row_key='id').classes('full-width') as table:
            table.add_slot('body', """
                <q-tr :props="props">
                    <q-td v-for="col in props.cols" :key="col.name" :props="props">
                        <q-icon v-if="col.name === 'status'"
                            :color="col.value ? 'primary' : 'warning'"
                            :name="col.value ? 'task_alt' : 'cancel'"
                             size="2rem"
                        />
                        <a  v-else-if="col.name === 'name'"
                            :href="'board/' + props.row.id"
                        >
                            {{ col.value }}
                        </a>
                        <q-btn v-else-if="col.name === 'actions'" v-for="action in col.value" : key="action"
                            round dense flat :icon="action" class="mr-2"
                         />
                        <span v-else>{{ col.value }}</span>
                    </q-td>
                </q-tr>
            """)
