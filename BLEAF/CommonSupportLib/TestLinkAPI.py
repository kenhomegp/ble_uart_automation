import testlink

class TestLink:
    
    def __init__(self, server_url='http://wsgdevops/testlink/lib/api/xmlrpc/v1/xmlrpc.php', devkey='ee723978e6622a4974b6023176d778a9', project_name='Buckland'):
        self.tls_helper = testlink.TestLinkHelper(server_url=server_url, devkey=devkey)
        self.tls_api = self.tls_helper.connect(testlink.TestlinkAPIClient)
        self.project_id = self.get_proj_id(project_name)
    
    def get_proj_id(self, proj_name):
        projects = self.tls_api.getProjects()
        proj_id = [project['id'] for project in projects if (project['name'] == proj_name)][0]
        return proj_id
    
    def get_test_plan_id(self, test_plan_name):
        tp_list = self.tls_api.getProjectTestPlans(self.project_id)
        tp_id = [tp['id'] for tp in tp_list if (tp['name'] == test_plan_name)][0]
        return tp_id
    
    def get_tests_in_test_plan(self,tp_id):
        test_case_dict = {}
        tc_dict = self.tls_api.getTestCasesForTestPlan(tp_id)
        print("TC_Dict: {}".format(tc_dict))
        print("TC_Dict_values: {}".format(tc_dict.values()))
        build = self.tls_api.getBuildsForTestPlan(tp_id)[0]['id']
        platformslist = self.tls_api.getTestPlanPlatforms(tp_id)
        for test_case in tc_dict.values():
            test_dic = {}
            test_dic['build'] = build
            test_dic['pltfrm'] = platformslist
            if isinstance(test_case,dict):
                platforms = list(test_case.keys())
                tc_name = test_case[platforms[0]]['tcase_name']
                tc_external_id = test_case[platforms[0]]['full_external_id']
                test_dic['id'] = tc_external_id
                platform_names = []
                for platform in platforms:
                    platform_name = test_case[platform]['platform_name']
                    platform_names.append(platform_name)
                test_dic['platforms'] = platform_names
                test_case_dict[tc_name] = test_dic
                
            elif isinstance(test_case, list):
                tc_name = test_case[0]['tcase_name']
                tc_external_id = test_case[0]['full_external_id']
                test_dic['id'] = tc_external_id
                test_dic['plarform'] = []
                test_case_dict[tc_name] = test_dic
        return test_case_dict
    
    def get_tests_to_execute(self, test_plan_name):
        tp_id = self.get_test_plan_id(test_plan_name)
        return self.get_tests_in_test_plan(tp_id)
    
    def post_test_result(self, testcaseid, testplanid, status, notes,build_id, platformname, overwrite=True):
        result = self.tls_api.reportTCResult(testcaseexternalid=testcaseid, testplanid=testplanid, status=status, notes=notes, overwrite=overwrite, buildid=build_id, platformname=platformname)
        print("Result:: {}".format(result))