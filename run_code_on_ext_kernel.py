import sys, os

JEROMQ_JAR = 'jeromq-0.3.5-SNAPSHOT.jar'

OTHER_JARS = ['guava-17.0.jar']


if os.name == 'java':
    # Running on Jython
    if not os.path.exists(JEROMQ_JAR):
        print 'Could not find {0} to add to sys.path'.format(JEROMQ_JAR)
        sys.exit()
    sys.path.append(JEROMQ_JAR)
    sys.path.extend(OTHER_JARS)


from IPython.kernel.connect import find_connection_file
from IPython.kernel.blocking.client import BlockingKernelClient

if len(sys.argv) != 2:
    print 'Usage:'
    print '  {0} <kernel_id>'.format(sys.argv[0])
    print ''
    print 'First, start an IPython kernel with regular CPython based IPython:'
    print '> ipython kernel'
    print ''
    print 'Take note of the kernel ID and pass it as the ID to this program'
    sys.exit()
else:
    kernel_id = sys.argv[1]

# this is a helper method for turning a fraction of a connection-file name
# into a full path.  If you already know the full path, you can just use that
cf = find_connection_file(kernel_id)

km = BlockingKernelClient(connection_file=cf)
# load connection info and init communication
km.load_connection_file()
km.start_channels()

def run_cell(km, code):
    # now we can run code.  This is done on the shell channel
    shell = km.shell_channel
    print
    print "running:"
    print code

    # execution is immediate and async, returning a UUID
    msg_id = shell.execute(code)
    # get_msg can block for a reply
    reply = shell.get_msg()

    status = reply['content']['status']
    if status == 'ok':
        print 'succeeded!'
    elif status == 'error':
        print 'failed!'
        for line in reply['content']['traceback']:
            print line

run_cell(km, 'a=5')
run_cell(km, 'b=0')
run_cell(km, 'c=a/b')