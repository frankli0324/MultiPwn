class FlagHandler:
    @staticmethod
    def get_result(flag):
        __import__('time').sleep(1)
        # simulates network latency
        try:
            if int(flag[5:9]) > 3000:
                return 'success'
            else:
                return 'wrong'
        except:
            return 'error'