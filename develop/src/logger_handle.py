import logging


def logger_handle(level=logging.ERROR, logger_file=None, formatter='%(asctime)s [%(levelname)8s] [%(module)s.%(funcName)s:%(lineno)d] %(message)s'):
    """
    logging.DEBUG     logging.debug('')
    logging.INFO      logging.info('')
    logging.WARNING   logging.warning('')
    logging.ERROR     logging.error('')
    logging.CRITICAL  logging.critical('')

    '[%(levelname)-8s] %(asctime)s %(message)s'
    '%(asctime)s %(levelname)-8s %(message)s'
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s'
    '%(asctime)s [%(levelname)8s] [%(process)d.%(thread)d.%(name)s.%(funcName)s:%(lineno)d] %(message)s'
    '%(asctime)s [%(levelname)8s] [%(module)s.%(funcName)s:%(lineno)d] %(message)s'

    Keyword Arguments:
        level {logging} -- logging level. (default: {logging.ERROR})
        logger_file {File pathname} -- save logger to file (default: {None})
        formatter {logger format} -- formatter (default: {%(asctime)s [%(levelname)8s] [%(module)s.%(funcName)s:%(lineno)d] %(message)s})
    """

    if logger_file != None:
        # set up logging to file - see previous section for more details
        logging.basicConfig(level=level,
                            format=formatter,
                            filename=logger_file)

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(level)
    # set a format which is simpler for console use
    formatter = logging.Formatter(formatter)
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)


if __name__ == '__main__':
    import sys
    logger_handle(level=logging.DEBUG, logger_file='%s.log' %
                  sys.argv[0].split('.')[0])

    logging.debug('debuge')
    logging.info('info')
    logging.warning('warning')
    logging.error('error')
    logging.critical('critical')
