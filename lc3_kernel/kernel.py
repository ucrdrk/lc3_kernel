from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF

import re
import tempfile
import subprocess

class Lc3Kernel(Kernel):
    implementation = 'LC-3'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {
        'name': 'lc3',
        'mimetype': 'text/plain',
        'file_extension': '.asm',
    }
    banner = "LC-3 kernel - useful for CS061 at UC Riverside"

    code_re = re.compile(r'^\.ORIG.*\.END$', re.DOTALL | re.I)

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.sim_wrapper = replwrap.REPLWrapper("/home/allan/cs061/ucrdrk-lc3tools/build/bin/simulator", 'instructions\r\n> ', '', '\r\n> ')

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            
            if Lc3Kernel.code_re.match(code) != None:
                with tempfile.NamedTemporaryFile(delete=False) as asm_file:
                  asm_file.write(code.encode('utf-8'))
                  asm_file.flush()
                  obj_result = subprocess.check_output(['/home/allan/cs061/ucrdrk-lc3tools/build/bin/assembler', asm_file.name])
                  response = obj_result.decode("utf-8")
                  response += self.sim_wrapper.run_command('load ' + asm_file.name + ".obj")
            else:
              match code:
                case 'quit': response = 'Unable to quit from cell'
                case _: response = self.sim_wrapper.run_command(code)  
              
            stream_content = {'name': 'stdout', 'text': response}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
