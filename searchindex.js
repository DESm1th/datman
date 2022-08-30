Search.setIndex({docnames:["api","api/datman","api/datman.config","api/datman.dashboard","api/datman.exceptions","api/datman.fs_log_scraper","api/datman.header_checks","api/datman.metrics","api/datman.scan","api/datman.scan_list","api/datman.scanid","api/datman.utils","api/datman.xnat","changes","datman_conf","index","installation","links"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,"sphinx.ext.intersphinx":1,sphinx:56},filenames:["api.rst","api/datman.rst","api/datman.config.rst","api/datman.dashboard.rst","api/datman.exceptions.rst","api/datman.fs_log_scraper.rst","api/datman.header_checks.rst","api/datman.metrics.rst","api/datman.scan.rst","api/datman.scan_list.rst","api/datman.scanid.rst","api/datman.utils.rst","api/datman.xnat.rst","changes.rst","datman_conf.rst","index.rst","installation.rst","links.rst"],objects:{"":[[1,0,0,"-","datman"]],"datman.config":[[2,1,1,"","TagInfo"],[2,1,1,"","config"],[2,5,1,"","study_required"]],"datman.config.TagInfo":[[2,2,1,"","get"],[2,2,1,"","keys"],[2,3,1,"","series_map"]],"datman.config.config":[[2,2,1,"","get_key"],[2,2,1,"","get_path"],[2,2,1,"","get_sites"],[2,2,1,"","get_study_base"],[2,2,1,"","get_study_tags"],[2,2,1,"","get_tags"],[2,2,1,"","get_xnat_projects"],[2,4,1,"","install_config"],[2,2,1,"","load_yaml"],[2,2,1,"","map_xnat_archive_to_project"],[2,2,1,"","set_study"],[2,4,1,"","study_config"],[2,4,1,"","study_config_file"],[2,4,1,"","study_name"],[2,4,1,"","system_config"]],"datman.dashboard":[[3,5,1,"","add_scan"],[3,5,1,"","add_session"],[3,5,1,"","add_subject"],[3,5,1,"","dashboard_required"],[3,5,1,"","filename_required"],[3,5,1,"","get_bids_scan"],[3,5,1,"","get_bids_subject"],[3,5,1,"","get_default_user"],[3,5,1,"","get_project"],[3,5,1,"","get_scan"],[3,5,1,"","get_session"],[3,5,1,"","get_study_subjects"],[3,5,1,"","get_subject"],[3,5,1,"","release_db"],[3,5,1,"","scanid_required"],[3,5,1,"","set_study_status"]],"datman.exceptions":[[4,6,1,"","ConfigException"],[4,6,1,"","DashboardException"],[4,6,1,"","ExportException"],[4,6,1,"","InputException"],[4,6,1,"","MetadataException"],[4,6,1,"","ParseException"],[4,6,1,"","QCException"],[4,6,1,"","UndefinedSetting"],[4,6,1,"","XnatException"]],"datman.exceptions.XnatException":[[4,4,1,"","message"],[4,4,1,"","session"],[4,4,1,"","study"]],"datman.fs_log_scraper":[[5,1,1,"","FSLog"],[5,5,1,"","check_diff"],[5,5,1,"","choose_standard_sub"],[5,5,1,"","make_standards"],[5,5,1,"","scrape_logs"],[5,5,1,"","verify_standards"]],"datman.fs_log_scraper.FSLog":[[5,2,1,"","get_args"],[5,2,1,"","get_date"],[5,2,1,"","get_kernel"],[5,2,1,"","get_niftis"],[5,2,1,"","get_subject"],[5,2,1,"","parse_recon_done"],[5,2,1,"","read_log"]],"datman.header_checks":[[6,5,1,"","check_bvals"],[6,5,1,"","compare_headers"],[6,5,1,"","construct_diffs"],[6,5,1,"","find_bvals"],[6,5,1,"","handle_diff"],[6,5,1,"","parse_file"],[6,5,1,"","read_json"],[6,5,1,"","remove_fields"],[6,5,1,"","write_diff_log"]],"datman.metrics":[[7,1,1,"","ABCDPHAMetrics"],[7,1,1,"","AnatMetrics"],[7,1,1,"","AnatPHAMetrics"],[7,1,1,"","DTIMetrics"],[7,1,1,"","DTIPHAMetrics"],[7,1,1,"","FMRIMetrics"],[7,1,1,"","FMRIPHAMetrics"],[7,1,1,"","IgnoreMetrics"],[7,1,1,"","Metric"],[7,1,1,"","MetricDTI"],[7,1,1,"","QAPHAMetrics"],[7,1,1,"","QCOutput"],[7,5,1,"","get_handlers"]],"datman.metrics.ABCDPHAMetrics":[[7,2,1,"","generate"],[7,4,1,"","outputs"]],"datman.metrics.AnatMetrics":[[7,2,1,"","generate"],[7,4,1,"","outputs"]],"datman.metrics.AnatPHAMetrics":[[7,2,1,"","generate"],[7,4,1,"","outputs"]],"datman.metrics.DTIMetrics":[[7,2,1,"","generate"],[7,4,1,"","outputs"]],"datman.metrics.DTIPHAMetrics":[[7,2,1,"","generate"],[7,4,1,"","outputs"]],"datman.metrics.FMRIMetrics":[[7,2,1,"","generate"],[7,4,1,"","outputs"]],"datman.metrics.FMRIPHAMetrics":[[7,2,1,"","generate"],[7,4,1,"","outputs"]],"datman.metrics.IgnoreMetrics":[[7,2,1,"","exists"],[7,2,1,"","generate"],[7,4,1,"","outputs"],[7,2,1,"","write_manifest"]],"datman.metrics.Metric":[[7,2,1,"","command_succeeded"],[7,2,1,"","exists"],[7,2,1,"","generate"],[7,2,1,"","get_requirements"],[7,2,1,"","is_runnable"],[7,2,1,"","make_image"],[7,2,1,"","make_manifest"],[7,2,1,"","make_montage"],[7,3,1,"","manifest_path"],[7,2,1,"","outputs"],[7,2,1,"","read_manifest"],[7,4,1,"","requires"],[7,2,1,"","run"],[7,2,1,"","set_outputs"],[7,2,1,"","write_manifest"]],"datman.metrics.QAPHAMetrics":[[7,2,1,"","generate"],[7,4,1,"","outputs"],[7,2,1,"","update_expected_outputs"]],"datman.metrics.QCOutput":[[7,4,1,"","caption"],[7,4,1,"","order"],[7,4,1,"","title"]],"datman.scan":[[8,1,1,"","DatmanNamed"],[8,1,1,"","Scan"],[8,1,1,"","Series"]],"datman.scan.Scan":[[8,2,1,"","get_tagged_nii"]],"datman.scan_list":[[9,1,1,"","ScanEntryABC"],[9,5,1,"","generate_scan_list"],[9,5,1,"","get_scan_list_contents"],[9,5,1,"","make_new_entries"],[9,5,1,"","start_new_scan_list"],[9,5,1,"","update_scans_csv"]],"datman.scan_list.ScanEntryABC":[[9,2,1,"","get_target_name"]],"datman.scanid":[[10,1,1,"","BIDSFile"],[10,1,1,"","DatmanIdentifier"],[10,1,1,"","Identifier"],[10,1,1,"","KCNIIdentifier"],[10,5,1,"","get_field"],[10,5,1,"","get_kcni_identifier"],[10,5,1,"","get_session_num"],[10,5,1,"","get_subid"],[10,5,1,"","is_phantom"],[10,5,1,"","is_scanid"],[10,5,1,"","is_scanid_with_session"],[10,5,1,"","make_filename"],[10,5,1,"","parse"],[10,5,1,"","parse_bids_filename"],[10,5,1,"","parse_filename"]],"datman.scanid.DatmanIdentifier":[[10,2,1,"","get_xnat_experiment_id"],[10,2,1,"","get_xnat_subject_id"],[10,4,1,"","pha_pattern"],[10,4,1,"","pha_re"],[10,4,1,"","scan_pattern"],[10,4,1,"","scan_re"],[10,3,1,"","session"]],"datman.scanid.Identifier":[[10,2,1,"","get_bids_name"],[10,2,1,"","get_full_subjectid"],[10,2,1,"","get_full_subjectid_with_timepoint"],[10,2,1,"","get_full_subjectid_with_timepoint_session"],[10,2,1,"","get_xnat_experiment_id"],[10,2,1,"","get_xnat_subject_id"],[10,2,1,"","match"]],"datman.scanid.KCNIIdentifier":[[10,2,1,"","get_xnat_experiment_id"],[10,2,1,"","get_xnat_subject_id"],[10,4,1,"","pha_pattern"],[10,4,1,"","pha_re"],[10,4,1,"","scan_pattern"],[10,4,1,"","scan_re"]],"datman.utils":[[11,1,1,"","XNATConnection"],[11,1,1,"","cd"],[11,5,1,"","check_dependency_configured"],[11,5,1,"","check_returncode"],[11,5,1,"","define_folder"],[11,5,1,"","filter_niftis"],[11,5,1,"","find_tech_notes"],[11,5,1,"","get_all_headers_in_folder"],[11,5,1,"","get_archive_headers"],[11,5,1,"","get_extension"],[11,5,1,"","get_files_with_tag"],[11,5,1,"","get_folder_headers"],[11,5,1,"","get_loaded_modules"],[11,5,1,"","get_relative_source"],[11,5,1,"","get_resources"],[11,5,1,"","get_subject_metadata"],[11,5,1,"","get_tarfile_headers"],[11,5,1,"","get_xnat_credentials"],[11,5,1,"","get_zipfile_headers"],[11,5,1,"","has_permissions"],[11,5,1,"","is_dicom"],[11,5,1,"","is_named_like_a_dicom"],[11,5,1,"","locate_metadata"],[11,5,1,"","make_temp_directory"],[11,5,1,"","make_zip"],[11,5,1,"","makedirs"],[11,5,1,"","nifti_basename"],[11,5,1,"","read_blacklist"],[11,5,1,"","read_checklist"],[11,5,1,"","read_credentials"],[11,5,1,"","remove_empty_files"],[11,5,1,"","run"],[11,5,1,"","run_dummy_q"],[11,5,1,"","split_path"],[11,5,1,"","splitext"],[11,5,1,"","submit_job"],[11,5,1,"","update_blacklist"],[11,5,1,"","update_checklist"],[11,5,1,"","validate_subject_id"],[11,5,1,"","write_metadata"]],"datman.xnat":[[12,1,1,"","XNATExperiment"],[12,1,1,"","XNATObject"],[12,1,1,"","XNATScan"],[12,1,1,"","XNATSubject"],[12,5,1,"","get_auth"],[12,5,1,"","get_connection"],[12,5,1,"","get_port_str"],[12,5,1,"","get_server"],[12,1,1,"","xnat"]],"datman.xnat.XNATExperiment":[[12,2,1,"","download"],[12,2,1,"","get_autorun_ids"],[12,2,1,"","get_resources"]],"datman.xnat.XNATScan":[[12,2,1,"","is_derived"],[12,2,1,"","is_multiecho"],[12,2,1,"","raw_dicoms_exist"],[12,2,1,"","set_datman_name"],[12,2,1,"","set_tag"]],"datman.xnat.xnat":[[12,4,1,"","auth"],[12,2,1,"","create_resource_folder"],[12,2,1,"","delete_resource"],[12,2,1,"","dismiss_autorun"],[12,2,1,"","find_project"],[12,2,1,"","find_subject"],[12,2,1,"","get_dicom"],[12,2,1,"","get_experiment"],[12,2,1,"","get_experiment_ids"],[12,2,1,"","get_projects"],[12,2,1,"","get_resource"],[12,2,1,"","get_resource_archive"],[12,2,1,"","get_resource_ids"],[12,2,1,"","get_resource_list"],[12,2,1,"","get_scan"],[12,2,1,"","get_scan_ids"],[12,2,1,"","get_subject"],[12,2,1,"","get_subject_ids"],[12,4,1,"","headers"],[12,2,1,"","make_experiment"],[12,2,1,"","make_subject"],[12,2,1,"","open_session"],[12,2,1,"","put_dicoms"],[12,2,1,"","put_resource"],[12,2,1,"","rename_experiment"],[12,2,1,"","rename_subject"],[12,4,1,"","server"],[12,4,1,"","session"]],datman:[[2,0,0,"-","config"],[3,0,0,"-","dashboard"],[4,0,0,"-","exceptions"],[5,0,0,"-","fs_log_scraper"],[6,0,0,"-","header_checks"],[7,0,0,"-","metrics"],[8,0,0,"-","scan"],[9,0,0,"-","scan_list"],[10,0,0,"-","scanid"],[11,0,0,"-","utils"],[12,0,0,"-","xnat"]]},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","property","Python property"],"4":["py","attribute","Python attribute"],"5":["py","function","Python function"],"6":["py","exception","Python exception"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:property","4":"py:attribute","5":"py:function","6":"py:exception"},terms:{"0":[10,11,14,15],"00":11,"02":15,"0rc1":15,"1":[7,10,11,12,14,15],"1000":14,"11":15,"111":14,"1111":14,"112":14,"1600":7,"16649196":15,"1_snr_adc":7,"2":[7,10,11,12,14,15],"2006":15,"2011":15,"2019":15,"2020":15,"212":15,"212_spectra":15,"22":14,"222":14,"23":15,"245":13,"247":13,"248":13,"250":13,"251":13,"252":13,"2_b0distortionratio":7,"3":[7,10,11,12,13,14,15],"333":14,"3_eddycurrentdistort":7,"4":[7,10],"443":14,"444":14,"4_avenyqratio":7,"5":[7,15],"59":15,"5_favalu":7,"6":[7,10,15],"60dir":14,"7":7,"777":14,"8":[7,10],"9":[7,10,14],"999":14,"abstract":[7,9,10],"boolean":14,"case":[2,10,14],"class":[0,2,5,7,8,9,10,11,12],"default":[2,4,7,8,10,11,12,14],"do":[10,11,12],"export":[14,16],"function":[0,2,3,6,7,9,10,11,14,15],"import":14,"int":[7,10],"long":3,"new":[12,14,15],"return":[2,3,7,9,10,11,12],"short":[14,15],"static":5,"super":9,"switch":[2,11],"true":[8,11,12,14],"try":14,"var":[11,14],"while":[3,10,12],A:[3,5,7,8,9,10,11,12,14,15],And:14,As:[2,10,14],At:14,By:2,For:[4,10,14,15],If:[2,7,10,11,12,14,16],In:14,It:[11,12,14,15],NOT:12,OR:11,On:16,One:[2,14],That:9,The:[2,5,7,8,9,10,11,12,14,15,16],These:[2,11,14,15,16],To:[9,14,15,16],Will:[11,12],_01:8,_:10,__init__:[2,9],_b0:7,_bad_fd:15,_corr:[7,15],_direct:7,_fd:[7,15],_imag:7,_montag:7,_plot:7,_qascripts_bold:[7,15],_qascripts_dti:[7,15],_raw:7,_scanlength:[7,15],_se:10,_session:8,_sfnr:[7,15],_spectra:[7,15],_spikecount:7,_stat:[7,15],abc:[7,10,12,14],abcd:[7,14],abcd_dmri:14,abcd_fmri:14,abcdphametr:7,abl:14,about:[5,8,11],abov:[14,15],absolut:[2,8,12,15],accept:[10,11,14],access:[8,11,12,14,16],accident:11,acq:10,acquisit:[10,14,15],across:15,act:14,action:12,activ:15,ad:12,adapt:2,add:[11,15,16],add_scan:3,add_sess:3,add_subject:3,addit:[2,11,16],address:14,adni:[7,15],afni:16,after:[3,8,11],again:14,against:14,aggreg:5,al:15,all:[2,8,10,11,12,13,14,15,16],alloc:11,allow:[2,10,14],allow_parti:11,alphanumer:10,alreadi:[9,12,14],also:[11,12,14,15,16],alwai:10,an:[2,3,10,11,12,14,15],anaconda:15,analysi:15,analyt:15,anat:14,anatmetr:7,anatphametr:7,ani:[5,7,8,10,11,12,14,16],anoth:[10,14],anotherxnat:14,anyth:14,api:[12,14,15],appear:12,appli:[3,10,12,14],applic:15,ar:[3,5,7,10,11,12,14,15,16],archiv:[2,11,12,14,15],argslist:11,argument:[3,11],aris:15,arm1:14,arm2:14,arm3:14,artifact:15,asid:10,assess:15,asset:[14,15,16],assign:14,associ:12,assum:[8,11,14],assur:15,attempt:[3,11,12],attend:14,attribut:8,auth:12,automat:15,autorun:12,avail:[14,16],averag:15,b0:[7,15],b0distort:7,b:11,back:[11,14],bad:15,base:[2,4,5,7,8,9,10,11,12,14],base_nam:12,basenam:11,becaus:[12,14],becom:[8,14,15],been:[2,7,11,16],befor:[11,12,14],begin:14,behavior:12,being:[11,14,15],belong:[11,12,14],below:[10,14,16],benefit:14,best:11,between:[2,5,7,14,15],bewar:12,bid:[10,11,14],bids_id:11,bids_nam:3,bids_s:11,bids_sess:3,bidsfil:10,bidsifi:14,bin:16,blacklist:[11,14],block:[11,14,16],bold:[7,15],bool:[11,12],both:2,boxx:14,brain:15,bravo:14,bug:13,bval:7,bvec:7,bytestr:13,c:11,ca:14,cach:12,calcul:15,call:[9,10,12],camelcas:14,can:[2,3,9,10,11,12,14,16],candid:11,capit:14,caption:7,care:11,caus:[10,11,12,14],cd:[11,15,16],ce:10,centralslic:7,certain:[8,10,12],chang:[8,10,11,12,13,14],charact:[10,14],chavez:15,check:[3,11],check_bval:6,check_dependency_configur:11,check_diff:5,check_returncod:11,checklist:[11,13,14],choose_standard_sub:5,chronolog:15,circumv:11,classmethod:7,clean:12,clevi:14,clock:11,clone:[15,16],cmd:11,cmd_arg:5,cmh:14,cmt:14,code:[3,9,10,11,13,14],col_head:5,collect:[11,14,15],com:[14,15,16],comma:11,command:[7,11,16],command_nam:7,command_succeed:7,comment:[11,14],comment_field:14,commit:3,compar:[6,14],compare_head:6,compil:10,complet:[3,11,12,14,15],complic:14,compon:11,comput:2,conda:15,conf_dir:16,config:[0,1,8,11,12,14,16],config_templ:14,configdir:[14,16],configexcept:4,configur:[2,11,12,15,16],conflict:2,conform:[10,11,12],connect:[3,12,14,15],consequ:12,consid:[2,11],consist:10,construct:14,construct_diff:6,consult:12,contact:14,contain:[5,9,10,11,12,14,15],content:[8,11,14],context:[11,14],convent:[8,10,11,12,14],convers:13,convert:[3,10,14],copi:[14,16],core:[11,14],correct:[3,9,11,14,15],correctli:[11,14,16],correl:[7,15],correspond:10,corrupt:15,could:15,count:14,cpu_cor:11,creat:[3,8,9,10,12,14,15,16],create_resource_fold:12,creation:12,cred_fil:11,credenti:16,criteria:3,csv:[7,9,11,14,15],current:[2,8,11,12,14,16],current_subid:10,cut:15,d:[11,15],dashboard:[0,1,4,11,14],dashboard_requir:3,dashboardexcept:[3,4],data:[11,12,14,15,16],data_dir:16,databas:[3,11,15],datatyp:15,date:[3,8,14],date_field:14,date_str:5,datman:[0,14,16],datman_asset:15,datman_id:9,datman_log:14,datmanassetsdir:[14,16],datmanidentifi:10,datmannam:8,datmanprojectsdir:[14,16],dcm2niix:16,dcm:14,decemb:15,decod:13,decor:3,decorrel:15,def:9,defaults_onli:2,defin:[2,4,7,9,11,12,14,15],define_fold:11,definit:[14,15],delet:[11,12],delete_resourc:12,depend:[11,14,15,16],deposit:12,deprec:13,deriv:9,describ:[10,14,16],descript:[3,10,11,14,15],design:15,dest_dir:9,dest_fold:12,dest_zip:11,destin:[9,11],detail:[5,10,11,14],detect:[14,16],determin:14,deviat:15,dicom:[9,10,11,12,14,15],dict:[7,10,11,12],dictat:11,dictionari:[2,7,10,11,12,14],diff:6,differ:[2,5,12,14,15],differenti:2,diffimg:7,diffmask:7,dir:[10,11],direct:[7,15],directli:[11,16],directori:[2,8,9,11,14,16],disabl:12,discov:2,dismiss:12,dismiss_autorun:12,displac:15,distinguish:[14,15],dm_config:[2,16],dm_link:13,dm_link_shared_id:14,dm_log_serv:14,dm_parse_ea:14,dm_parse_gngo:14,dm_parse_nback:14,dm_qc_report:[14,16],dm_redcap_scan_complet:[14,16],dm_sftp:[14,16],dm_system:[2,11,14,16],dm_task_fil:[13,14],dm_xnat_extract:[14,16],dm_xnat_upload:14,docker:15,doe:[8,10,11,12,14,15,16],doesn:[11,12,14,15],doesnt:[10,11,12,14],domain:14,don:[3,11,15,16],done:11,dont:11,download:[12,14],downstream:11,drift:15,drift_bx:15,driftperc:15,drop:11,dryrun:11,dti01:10,dti15t:2,dti3t:2,dti60:14,dti:[2,6,7,10,14,15],dtimetr:7,dtiphametr:7,due:16,dure:[14,15],e:[2,3,8,10,11,14,16],each:[9,11,12,14,15],easi:8,echo:[10,14],echonumb:14,eddycurrentdist:7,either:[2,3,11,14],elsewher:14,empti:[5,11,12],enabl:2,encod:15,end:[3,14],endpoint:14,enough:9,ensur:[3,10,11],entir:11,entri:[9,11,14],entryclass:9,env:[14,15],env_var:11,environ:[2,11,12,14,15,16],environmenterror:11,ep2d:14,error:4,et:15,etc:[11,14,15],even:[11,12],event:14,everi:[2,14],exact:[2,7],exactli:14,exam:[11,15],exampl:[9,10,11,15],examplescanentri:9,except:[0,1,2,11,12,14],excerpt:14,exclud:10,exist:[2,7,11,12,14,15],exit:[3,11],expect:[2,3,5,6,7,9,11,14],expected_kei:5,exper_id:12,experi:12,experienc:12,experiment_json:12,experiment_nam:12,export_set:2,exportexcept:4,exportinfo:2,exportset:2,ext:10,extens:11,extract:2,f:3,fail:[11,12],failur:[11,12],fals:[2,3,5,6,7,11,12,14],fbirn:[7,15],fbrin:15,fd:15,fewer:14,field:[2,5,6,9,10,11,14],file:[2,3,5,6,7,8,9,10,11,12,15,16],file_path:[6,12],filenam:[2,11,12],filename_requir:3,fileobj:11,filesystem:11,filter:3,filter_nifti:11,find:[10,11,12,14],find_bval:6,find_project:12,find_subject:12,find_tech_not:11,findabl:11,finish:12,first:[2,3,11,12,13,14],fit:14,fix:13,flag:[10,11,16],fluctuat:15,fmap:14,fmri:[7,14,15],fmrimetr:7,fmriphametr:7,folder:[2,5,11,12,14,15,16],foldernam:12,follow:[14,15],fool:11,form:14,format:[8,9,10,11,12,14],found:[2,3,5,11,12,14],fpath:11,framewis:15,freeform:14,freesurf:5,freesurfer_fold:5,friedman:15,from:[2,3,5,7,8,10,11,12,13,14,15,16],fs_log_scrap:[0,1],fs_output_fold:5,fsl:[7,16],fslog:5,ftpport:14,ftpserver:14,full:[2,7,10,11,14,16],fulli:[11,14],fullnam:14,further:15,fuzzi:11,g:[2,3,8,10,14,16],gap:7,gener:[5,7,9,11,14,15,16],generate_scan_list:9,get:[2,3,10,11,12,14],get_all_headers_in_fold:11,get_archive_head:11,get_arg:5,get_auth:12,get_autorun_id:12,get_bids_nam:10,get_bids_scan:3,get_bids_subject:3,get_connect:12,get_dat:5,get_default_us:3,get_dicom:12,get_experi:12,get_experiment_id:12,get_extens:11,get_field:10,get_files_with_tag:11,get_folder_head:11,get_full_subjectid:10,get_full_subjectid_with_timepoint:10,get_full_subjectid_with_timepoint_sess:10,get_handl:7,get_kcni_identifi:10,get_kei:2,get_kernel:5,get_loaded_modul:11,get_nifti:5,get_path:2,get_port_str:12,get_project:[3,12],get_relative_sourc:11,get_requir:7,get_resourc:[11,12],get_resource_arch:12,get_resource_id:12,get_resource_list:12,get_scan:[3,12],get_scan_id:12,get_scan_list_cont:9,get_serv:12,get_sess:3,get_session_num:10,get_sit:2,get_study_bas:2,get_study_subject:3,get_study_tag:2,get_subid:10,get_subject:[3,5,12],get_subject_id:12,get_subject_metadata:11,get_tag:2,get_tagged_nii:8,get_tarfile_head:11,get_target_nam:9,get_xnat_credenti:11,get_xnat_experiment_id:10,get_xnat_project:2,get_xnat_subject_id:10,get_zipfile_head:11,git:[15,16],github:[13,15,16],give:[2,12,14],given:[2,3,7,8,10,11,12,14],global:[14,15],global_corr:15,glossari:15,gmean:15,gmean_bx:15,go:[11,14],goe:[9,14],gold:[6,14],good:15,gov:15,grab:12,grace:11,grappa:14,greatli:12,group:10,guess:11,gui:12,gz:[7,11,15],ha:[2,3,11,12,14],hand:14,handle_diff:6,happen:3,has_permiss:11,have:[11,14,15,16],haven:7,head:15,header:[6,9,10,11,12,14,15],header_check:[0,1],help:[3,14],here:[9,10,14,15,16],higher:15,hold:[8,11,14,16],how:[10,14],howev:14,html:15,http:[14,15,16],httperror:12,human:[14,15],i:[2,11,14],id:[2,3,4,8,9,10,11,12,14,16],ident:[8,10,14],identif:10,identifi:[2,3,8,10,11,12,15],idl:3,idtyp:10,ignor:[6,11,14],ignore_default:2,ignored_field:6,ignoremetr:7,imag:[7,11,14,15],imagetyp:14,img_gap:7,imposs:12,includ:[8,10,11,14,16],incorrect:11,index:15,indic:[11,14],info:[10,14],inform:[0,3,5,8,9,14,15],initi:11,input:7,input_nii:7,inputexcept:4,insert:7,insid:14,instal:[2,11,14,15],install_config:2,instanc:[2,3,8,9,10,11,12,15],instantan:15,instead:[11,13,14,16],instrument:14,integ:14,integr:[11,14,16],intend:9,intens:15,intensitii:15,interact:[12,14,16],interchang:12,interest:[11,12],interf:12,interfac:15,ip:14,is_complet:14,is_deriv:12,is_dicom:11,is_multiecho:12,is_named_like_a_dicom:11,is_open:3,is_phantom:10,is_runn:7,is_scanid:10,is_scanid_with_sess:10,isn:3,isnt:[3,11],isopen:14,issu:[4,16],item:11,its:[10,14],itself:[2,14],j:15,januari:15,job:[11,14],job_nam:11,joblist:11,join:2,jonathan:15,jpg:7,json:[6,14],json_cont:6,json_fil:6,json_path:6,just:[2,11,13,14,16],kcni:[10,14],kcniidentifi:10,keep:14,kei:[2,10,14],kept:14,keyerror:12,keyword:15,kind:15,know:15,kwarg:3,l:15,label:[12,14],lack:11,larg:[15,16],last:14,launch:12,lead:11,least:[2,14],left:[5,14],less:14,letter:14,level:[1,14,15],librari:[9,15],licens:16,like:[12,14],line:[5,11,14,16],linear:15,link:[14,15],linux:16,list:[3,5,9,11,12,14,16],list_of_nam:11,listen:14,liter:14,ll:16,load:11,load_yaml:2,loadedmodul:11,local:[2,14,16],locat:[2,3,11,14],locate_metadata:11,log:[5,11],log_dir:11,log_field:5,log_unam:5,logserv:14,logserverdir:14,look:[11,15],low:15,lowest:15,machin:14,made:[8,12],mag1:14,mag2:14,magn:15,magphan_adni_manu:15,mai:[8,11,14],main:[2,14,16],main_config:[14,16],maintain:10,major:15,make:[8,9,11,12,16],make_experi:12,make_filenam:10,make_imag:7,make_manifest:7,make_montag:7,make_new_entri:9,make_standard:5,make_subject:12,make_temp_directori:11,make_zip:11,makedir:11,manag:[9,10,11,14,15,16],mangl:[10,11,14],manifest_path:7,map:[2,7,10,11,12,14],map_xnat_archive_to_project:2,mark:12,maskcentralslic:7,match:[2,3,8,10,11,12,14,15],matlab:16,matlabpath:15,maxabsrm:15,maximum:15,maxrelrm:15,mean:[14,15],mean_fd:15,mean_sfnr:15,meanabsrm:15,meanrelrm:15,meant:[12,14],measur:15,measures:15,mem:11,merg:2,messag:[4,11,14],meta:14,metadata:12,metadata_path:9,metadataexcept:[4,11],method:[0,10,14],metric:[0,1,14,15],metricdti:7,might:10,mind:14,miss:8,mm:15,mnc:14,mod:10,modal:[10,15],modifi:[10,12,13,14],modul:[0,1,15],montag:7,more:[10,11,12,14,15],most:[2,5,14,15],mostli:12,motion:15,mount:14,mr:10,mrfolder:14,mrftppass:14,mri:[14,15],mruser:14,multicent:15,multipl:[2,3,10,11,14],mung:11,must:[7,11,14],my_instru:14,my_zip_list:9,myftppass:14,myproject:14,myredcapserv:14,myriad:15,myscan:14,mysftp:14,mystudi:14,mystudy_ut1:14,mysystem:14,mytoken:14,myuser:14,myxnat:14,n_bad_fd:15,name:[2,3,7,8,9,10,11,12,14,15,16],nativ:10,nb0:15,ncbi:15,nd:14,ndir:15,need:[7,12,14,15,16],network:15,neuroimag:15,new_entri:9,new_nam:12,next:14,nf:14,nibabel:15,nicknam:11,nifti:[6,7,8,14,15],nifti_basenam:11,nightli:14,nih:15,nii:[7,11,14,15],nii_input:7,nlm:15,nois:15,non:[10,11,12,14],none:[2,3,4,5,6,7,10,11,12],norm:14,note:[11,12,14,16],noth:12,nrrd:14,num:10,number:[10,11,14,15],numer:10,nyquistratio:7,obei:8,object:[2,5,7,8,9,10,11,12],obnoxi:12,obtain:15,obvious:12,off:[11,15],old_nam:12,omit:14,ommit:11,onc:[14,16],one:[10,11,12,14,15],ones:[13,15],onli:[2,11,12,14,15],onto:2,open:[3,12],open_sess:12,open_zipfil:11,oper:3,option:[3,7,10,11,12,16],order:[7,11],organ:[11,12,14],orig_id:10,origin:[10,11,14],os:[2,11],oserror:11,other:[10,11,12,14,15,16],otherwis:[11,14],otherxnat:14,our:[14,15],out:[8,14,16],outcount:15,outcount_bx:15,outlier:15,outmax:15,outmax_bx:15,outmean_bx:15,outmin:15,output:[5,7,9,11,12,14,16],output_dir:7,output_path:6,outsid:14,over:15,overrid:[2,15],overridden:[2,14],overwrit:[7,15],overwritten:11,own:[12,14,16],p:[10,14],packag:[0,15],page:15,pair:14,par:7,par_id:14,paramet:[3,5,7,8,10,11,12,14],parent:[8,11,12,14],parentdir:11,pars:[4,5,10,11,12,15],parse_bids_filenam:10,parse_fil:6,parse_filenam:[10,11],parse_recon_don:5,parseexcept:[4,8,10,11],part:[2,11,14],partial:11,particip:4,partit:11,pass:[9,11],password:[11,12,14,16],path:[2,5,7,8,10,11,12,16],path_typ:2,patientnam:9,pattern:2,pdf:[11,15],pep8:13,per:[14,15],perform:15,permiss:11,person:11,pha:10,pha_:10,pha_pattern:10,pha_r:10,pha_typ:10,phantom:[3,10,14,15],phantomlab:15,pip:16,pipelin:[11,12,14,15],pixel:7,place:[14,15],plan:16,pleas:[2,15],plot:7,png:7,pngappend:7,point:[14,15],port:[12,14],portion:[10,14],portnum:12,possibl:2,post:12,power:15,practic:[11,15],pre:[14,15],prearchiv:15,prefer:14,preferenti:11,prefix:[11,15],present:14,preserv:[11,14],prevent:[12,14],primari:15,primarycontact:14,problem:15,process:[11,15],processed_scan:9,produc:12,program:[11,15],program_nam:11,project:[2,12,15],project_set:8,projectdir:14,properti:[2,7,10],protocol:15,provid:[11,14,16],pubm:15,pull:[3,13,14],put:11,put_dicom:12,put_resourc:12,py:[2,13,14,15,16],python3:13,python:[11,13,14,15],pythonpath:15,qa:[7,15],qa_dti:14,qaphametr:7,qascript:15,qc:[7,11,14,15],qc_:15,qcexcept:[4,7],qcing:15,qcmon:[15,16],qcoutput:7,qcpha:14,qctype:14,qualifi:14,queri:12,queu:[11,12],queue:[11,14],ra:14,radiu:15,rais:[2,3,7,8,10,11,12],ran:16,rather:[15,16],ratio:15,raw:[14,15],raw_dicoms_exist:12,re:[2,10,11,15],read:[2,3,11,12,14,15],read_blacklist:11,read_checklist:11,read_credenti:11,read_json:6,read_log:5,read_manifest:7,readabl:14,real:11,rec:10,receiv:[3,14],recon_don:5,record:14,record_id_field:14,recurs:11,redcap:[13,16],redcap_token:[14,16],redcapapi:14,redcapcom:14,redcapd:14,redcapeventid:14,redcapinstru:14,redcapprojectid:14,redcaprecordkei:14,redcapstatu:14,redcapstatusvalu:14,redcapsubj:14,redcaptoken:14,redcapurl:14,redefin:14,ref:13,refer:[12,14],regex:14,reject:10,rel:[5,14,15],releas:13,release_db:3,remotelogin:14,remoteprojectid:14,remov:[11,13],remove_empty_fil:11,remove_field:6,renam:12,rename_exp:12,rename_experi:12,rename_subject:12,repeatedli:11,replac:16,report:[5,12,14,15],request:12,requir:[7,12,15,16],reson:15,resourc:[12,14],resource_group_id:12,resource_id:12,respect:14,respons:12,rest:15,restrict:[2,10,12],result:[2,7,10],retri:[11,12],retriev:[10,12,14,16],returncod:11,reus:3,revers:14,right:14,roi:15,rollback:3,root:[15,16],rootdir:16,round:13,rst:14,run:[3,5,7,10,11,12,14,15,16],run_dummy_q:11,s1:15,s2:15,s3:15,s4:15,s5:15,s:[2,3,7,10,11,12,14,15,16],sag:14,same:[3,11,12,14,15],save:[9,11],scan:[0,1,7,9,10,11,12,14,15],scan_entry_class:9,scan_id:12,scan_json:12,scan_list:[0,1],scan_path:9,scan_pattern:10,scan_r:10,scanentryabc:9,scanid:[0,1,3,8,11,13],scanid_requir:3,scanlength:7,scans_csv:9,scheme:[8,14],scipi:15,scrape:5,scrape_log:5,script:[3,5,9,11,13,14,15,16],se:10,search:[2,11,12,14,15],second:14,section2:7,section:14,see:[10,11,14,15],seemingli:12,self:[7,9],sensit:[10,14],separ:[11,14],seri:[3,6,8,10,11,14,15],series_json:6,series_map:2,series_path:6,seriesdescript:[10,14],server:[12,14],server_cach:12,serverlogdir:14,session:[2,4,7,8,10,11,12,14],set:[2,3,7,8,10,11,12,15,16],set_datman_nam:12,set_output:7,set_studi:2,set_study_statu:3,set_tag:12,setup:15,sfnr:7,sftp:14,sge:14,share:2,shell:[11,14],shell_cmd:11,should:[9,10,11,12,14,16],show:14,shown:16,side:14,sign:11,signal:15,similar:[10,11],sinc:11,singl:[7,8,10,11,12,14,15,16],sit:15,site:[2,3,10,11,12],site_set:2,sitetag:2,size:7,slice:7,slicer:7,slightli:11,slurm:[11,14],small:14,snr:15,snrimg:7,so:[2,11,12,15],sofia:15,softwar:16,some:[10,16],somefold:14,sometim:12,sophist:11,sourc:[2,3,4,5,6,7,8,9,10,11,12,14],source_dir:11,source_id:3,space:11,special:11,specialquot:11,specif:[0,2,3,11,12,14,16],specifi:[2,3,10,11,12,14],spectra:15,spikecount:7,spin:[2,3,14],split:[11,14],split_path:11,splitext:11,spn01:[2,3],spn01_zhh_0018_01_01_rst_06_rest:15,sprl:14,spuriou:15,squar:15,stack:15,standard:[5,6,14,15],standard_json:6,standard_log:5,standard_path:6,standards_dict:5,standards_field:5,start:14,start_new_scan_list:9,state:[3,12,15],statu:12,std:14,stdout:11,stdplotshist:7,still:[7,14,16],stop_after_first:11,store:[12,14],str:[7,10,11,12],string:[3,7,10,11,12,14],stroke:15,structur:[12,14,15],stu01:14,stu01_uto_10001_01_se01_mr:14,stuck:[3,12],studi:[2,3,4,10,11,12,15,16],study1:14,study1_config:14,study1_ut2_abc0001_01_01:14,study_config:[2,14],study_config_fil:2,study_nam:2,study_nicknam:16,study_requir:2,study_site_id_timepoint:8,studya:14,studyb:14,studyb_cmh:14,studyc:14,studytag:[2,14],style:[3,10,11,14],sub:4,sub_id_field:14,subclass:[9,10],subfold:[11,12],subject:[3,5,7,8,9,10,11,12,13,14,15],subject_field:5,subject_id:[8,11,12],subject_json:12,subject_log:5,subject_nam:12,submit:[11,14],submit_job:11,submodul:0,subset:14,success:[11,12],suffix:[10,11],suppli:[2,11],support:[10,11],survei:14,system:[2,11,14,16],system_config:2,systemat:[9,15],systemset:16,t1:[14,15],t2:14,t2w_spc_vnav:14,t:[3,7,10,11,12,14,15,16],tabl:14,tag:[2,3,8,10,11,14,15],tag_map:12,taginfo:2,take:[2,5,11,14,15],taken:15,tar:11,tarbal:[11,15],target:11,task:[10,14],tech:11,technic:10,technot:11,tempfil:12,templat:14,tempor:15,temporari:[12,14],tend:12,termin:3,test:14,than:[12,14,16],thei:[2,11,14,15],them:[2,10,12,14],thi:[2,3,8,9,10,11,12,14,15,16],thing:15,those:10,though:[12,16],three:[7,14,15],through:[12,15],tigrlab:[15,16],tigrlab_scan_completed_complet:14,time:[10,11,15],timepoint:10,timeseri:15,titl:[7,14],tmp:[11,14],todai:15,token:[14,16],toler:6,top:1,tr:15,track:15,transact:3,translat:[10,14],treat:14,tsnr:15,tsnr_bx:15,tumor:15,tupl:[10,12],two:[2,14,15],txt:[11,14],type:[2,7,10,11,12,14,15,16],typo:14,u:16,unabl:12,unassign:15,undefin:14,undefinedset:[2,4],under:[12,15],unexpect:12,uniform:8,uniqu:14,unless:11,unlik:14,unset:[12,14],until:[3,11],up:[11,12,14,15],updat:[11,13,16],update_blacklist:11,update_checklist:11,update_expected_output:7,update_scans_csv:9,upload:[12,14],uri:12,url:[12,14],us:[2,4,5,7,9,10,11,12,14,15,16],use_bid:11,user:[10,12,14,16],user_nam:11,usernam:[12,14,16],usesredcap:14,usual:14,ut1:[10,14],ut2:[10,14],util:[0,1,6,16],uto:[10,14],v:16,valid:[10,12],validate_subject_id:11,valu:[2,6,8,10,11,14,15],variabl:[2,11,12,13,14,16],variou:14,vector:15,verbos:11,verifi:11,verify_standard:5,versa:14,version:[11,13],versu:12,vice:14,visual:7,voxel:15,wa:[2,11,14,15],wai:[9,14,16],wait:3,walltim:11,want:[10,11,16],warn:8,we:[11,15],weight:15,well:3,were:[11,14],what:[14,15],whatev:14,when:[3,9,10,11,12,14,15],where:[2,9,11,12,14],whether:[11,12,14],which:[2,11,14,15],who:[10,11,14,16],whole:15,wide:[2,12],width:7,wish:11,within:[3,10,11,12,14,16],without:[2,11,15,16],work:[3,11],workdir:11,workflow:12,would:14,wrap:3,wrapper:2,write:[7,11,14,15],write_diff_log:6,write_manifest:7,write_metadata:11,wrong:9,www:15,x:11,xml:12,xnat:[0,1,2,4,15,16],xnat_connect:12,xnat_cr:11,xnat_fetch_sess:14,xnat_pass:[14,16],xnat_url:11,xnat_us:[14,16],xnatarch:14,xnatconnect:11,xnatconvent:14,xnatcredenti:14,xnatexcept:[4,12],xnatexperi:12,xnatlogin:14,xnatobject:12,xnatport:[12,14],xnatscan:12,xnatserv:14,xnatsourc:14,xnatsourcearch:14,xnatsourcecredenti:14,xnatsubject:12,xxx:14,yaml:[2,14],yet:11,yml:[8,14,16],you:[2,10,11,14,15,16],your:[14,15,16],yrk:14,z0:10,z:10,zero:11,zip:[9,11,12,14],zip_fil:9,zip_nam:12,zipfil:[11,12,15]},titles:["Library API (application program interface)","datman package","datman.config module","datman.dashboard module","datman.exceptions module","datman.fs_log_scraper module","datman.header_checks module","datman.metrics module","datman.scan module","datman.scan_list module","datman.scanid module","datman.utils module","datman.xnat module","What\u2019s new?","Configuration Files","datman","Installation","&lt;no title&gt;"],titleterms:{"0":13,"02":13,"0rc1":13,"1":13,"11":13,"2":13,"2019":13,"2020":13,"new":13,api:0,applic:0,config:2,configur:14,contain:16,control:15,dashboard:3,datman:[1,2,3,4,5,6,7,8,9,10,11,12,15],decemb:13,docker:16,exampl:14,except:4,exportinfo:14,exportset:14,file:14,fs_log_scrap:5,ftp:14,glossari:14,header_check:6,idmap:14,indic:15,instal:16,interfac:0,introduct:15,januari:13,librari:0,log:14,metadata:14,metric:7,modul:[2,3,4,5,6,7,8,9,10,11,12],option:14,overrid:14,overview:15,packag:1,path:14,pattern:14,program:0,project:14,qualiti:15,redcap:14,requir:14,s:13,scan:8,scan_list:9,scanid:10,set:14,site:14,studi:14,submodul:1,systemset:14,tabl:15,util:11,what:13,xnat:[12,14]}})