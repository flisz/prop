from project.setup.loggers import LOGGERS, init_loggers

init_loggers()
log = LOGGERS.Setup

from project.setup.environment import ENV



log.debug('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__, __name__, str(__package__)))


if any(__name__ == case for case in ['__main__', 'project']):
    from project.app import create_app
    app = create_app()
    app.run(host='127.0.0.1', port=5000)
