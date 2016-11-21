/**
 * Created by Guibin on 2016/3/19.
 */

//实现复选框全选与反选；
function checkAll(chkall) {
    if(chkall.checked){
        $("input[name='minion_id']").each(function(){this.checked=true;});
    }else{
        $("input[name='minion_id']").each(function(){this.checked=false;});
    }
}

function checkAllMinions(chkall) {
    if(chkall.checked){
        $("input[name='minions_ip']").each(function(){this.checked=true;});
    }else{
        $("input[name='minions_ip']").each(function(){this.checked=false;});
    }
}


//获取复选框的值
function getCheckValue(action) {
    var minion_id = "";
    $('input[name="minion_id"]:checked').each(function(){
        minion_id += $(this).val() + ',';
    });
    if (minion_id === "") {
        alert("您尚未选择任何选项，请重新选择后提交！");
        return false;
    } else {
        var url = '/keys/' + action + '/'
        $.getJSON(url, {"minion_id": minion_id, "action": action}, function(result) {
            if (result === true) {
                var ret = deleteTbodyTr(minion_id);
                if (ret === true) {
                    alert('操作成功！')
                } else {
                    alert('错误1：操作失败！')
                }

            } else {
                alert('错误2：操作失败！')
            }
        });
    }
}

//将'aaa,bbb,ccc,'转换为数组，并以此删除以此为id的元素；
function deleteTbodyTr(minion_id) {
    var minion_id_str = minion_id.slice(0,-1);
    var minion_id_array = minion_id_str.split(',');
    $.each(minion_id_array, function(index,value) {
        var tbody_tr_id = '#' + value;
        $(tbody_tr_id).remove();
    });
    return true;
}

function saltExecute() {
// $.ajaxSettings.async = false;
    $(document).ready(function(){
        $('#result').html("");
        $('#info').html("")
        var tgt = $("input[name='tgt']").val();
        var arg = $("input[name='arg']").val();
        var datacenter = "";
        $('input[name="datacenter"]:checked').each(function(){
            datacenter += $(this).val() + ',';
        });
        if ((tgt === '' || tgt === null) && (datacenter === '' || datacenter === null)) {
            alert('请输入服务器IP或选择对应机房！');
            return false;
        }
        if (arg === '' || arg === null) {
            alert('请输入将要执行的命令！');
            return false;
        }
        $("#execapi").attr("disabled","disabled");
        $("#execapi").html('<img src="/static/img/button.gif" style="width:28px;height:16px;"/>');
        $.getJSON("/salt/api/execute/",{'tgt':tgt,'datacenter':datacenter, 'arg': arg}, function(ret){
            if (ret.hasOwnProperty('errors')) {
                alert(ret.errors);
                $("#execapi").removeAttr("disabled");
                $("#execapi").html("提交");
                return false;
            } else {
                if (ret.info.unrecv_count===0) {
                    $('#info').html("本次执行对象共"+ret.info.send_count+"台，其中"+ret.info.recv_count+"台返回结果;"
                      );
                } else {
                    $('#info').html("本次执行对象共" + ret.info.send_count + "台，其中" + ret.info.recv_count + "台返回结果；未返回结果的有以下" + ret.info.unrecv_count + "台：<br/>" + ret.info.unrecv_strings
                      );
                }
                    var sortArray = [];
                $.each(ret.result, function(key, val) { sortArray[sortArray.length] = key;});
                sortArray.sort();
                $.each(sortArray, function(i, key) {
                    $("#result").append(
                            "<hr/><p class='bg-info'><b>" + key + "</b></p><pre>"+ret['result'][key]['cont']+"</pre>"
                    );
                });
            };
            $("#execapi").removeAttr("disabled");
            $("#execapi").html("提交");
        });
    });
    // $.ajaxSettings.async = true;
}

$(document).ready(function() {
	$(".stroage_ceph_check").click(function() {
		console.log("storage ceph check");
		if ($(this).is(":checked")) {
			console.log("ceph check");
			$("#storage_glusterfs").css({"display": "none"});
			$("#storage_ceph_mon").css({"display": ""});
			$("#storage_ceph_osd").css({"display": ""});
		}
	});
	
	$(".storage_glusterfs_check").click(function() {
		console.log("storage glusterfs check");
		if ($(this).is(":checked")) {
			console.log("glusterfs check");
			$("#storage_glusterfs").css({"display": ""});
			$("#storage_ceph_mon").css({"display": "none"});
			$("#storage_ceph_osd").css({"display": "none"});
		}
	});
	
	$(".neutron_vlan").click(function() {
		console.log("neutron vlan check");
		if ($(this).is(":checked")) {
			console.log("vlan check");
			$("#neutron_vlan").css({"display": ""});
			$("#neutron_vxlan").css({"display": "none"});
			$("#data_cidr").css({"display": "none"});
			$("#public_interface").css({"display": "none"});
			$("input[name='public_interface']").val("");
		}
	});
	
	$(".neutron_vxlan").click(function() {
		console.log("neutron vxlan check");
		if ($(this).is(":checked")) {
			console.log("vxlan check");
			$("#neutron_vlan").css({"display": "none"});
			$("#neutron_vxlan").css({"display": ""});
			$("#data_cidr").css({"display": ""});
			$("#public_interface").css({"display": ""});
		}
	});
	
	$("#storage_interface").blur(function() {
		console.log("storage interface mouseleave");
		var s_int = $(this).val();
		var m_int = $("#manage_interface").val();
		var d_int = $("#data_interface").val();
		
		if ($(".neutron_vxlan").is(":checked")) {
			if (s_int == m_int && s_int == d_int) {
				$("#data_cidr").css({"display": "none"});
				$("#storage_cidr").css({"display": "none"});
			}
			else if (s_int == m_int && s_int != d_int) {
				$("#data_cidr").css({"display": ""});
				$("#storage_cidr").css({"display": "none"});
			}
			else if (s_int != m_int && s_int == d_int) {
				$("#data_cidr").css({"display": "none"});
				$("#storage_cidr").css({"display": ""});
			}
			else if (s_int != m_int && s_int != d_int) {
				if (m_int == d_int) {
					$("#data_cidr").css({"display": "none"});
					$("#storage_cidr").css({"display": ""});
				}
				else {
					$("#data_cidr").css({"display": ""});
					$("#storage_cidr").css({"display": ""});
				}
			}
		}
		else if ($(".neutron_vlan").is(":checked")) {
			if (s_int == m_int) {
				console.info("manage interface equal to storage interface");
				$("#storage_cidr").css({"display": "none"});
			}
			else {
				console.info("manage interface not equal to storage interface");
				$("#storage_cidr").css({"display": ""});
			}
		}
	});
	
	$("#manage_interface").blur(function() {
		console.info("manage interface blur");
		var m_int = $(this).val();
		var s_int = $("#storage_interface").val();
		var d_int = $("#data_interface").val();
		
		if ($(".neutron_vxlan").is(":checked")) {
			if (m_int == s_int && m_int == d_int) {
				$("#data_cidr").css({"display": "none"});
				$("#storage_cidr").css({"display": "none"});
			}
			else if (m_int == s_int && m_int != d_int) {
				$("#data_cidr").css({"display": ""});
				$("#storage_cidr").css({"display": "none"});
			}
			else if (m_int != s_int && m_int == d_int) {
				$("#data_cidr").css({"display": "none"});
				$("#storage_cidr").css({"display": ""});
			}
			else if (m_int != s_int && m_int != d_int) {
				if (s_int == d_int) {
					$("#data_cidr").css({"display": "none"});
				}
				else {
					$("#data_cidr").css({"display": ""});
					$("#storage_cidr").css({"display": ""});
				}
			}
		}
		else if ($(".neutron_vlan").is(":checked")) {
			if (m_int == s_int) {
				console.info("manage interface equal to storage interface");
				$("#storage_cidr").css({"display": "none"});
			}
			else {
				console.info("manage interface not equal to storage interface");
				$("#storage_cidr").css({"display": ""});
			}
			$("#data_cidr").css({"display": "none"});
		}
	});
	
	$("#data_interface").blur(function() {
		console.info("data interface mouseleave");
		var d_int = $(this).val();
		var s_int = $("#storage_interface").val();
		var m_int = $("#manage_interface").val();
		
		if ($(".neutron_vxlan").is(":checked")) {
			if (d_int == m_int) {
				console.log("data interface equal to manage interface");
				$("#data_cidr").css({"display": "none"});
			}
			else if (d_int == s_int) {
				$("#data_cidr").css({"display": "none"});
			}
			else {
				$("#data_cidr").css({"display": ""});
			}
		}
		else if ($(".neutron_vlan").is(":checked")) {
			$("#data_cidr").css({"display": "none"});
		}
	});
});


$(document).ready(function() {
  $(".sev_check").click(function() {
	  if ($('.ha_check').is(":checked")) {
		  console.log("enable ha");
	  }
	  else{
		  console.log("not enable ha");
		  if ($(this).is(":checked")) {
		        var group = "input:checkbox[name='" + $(this).attr("name") + "']";
		        $(group).prop("checked", false);
		        $(this).prop("checked", true);
		    } else {
		        $(this).prop("checked", false);
		    }
	  }
  });
});


function choose_one_checkbox(obj) {
	 if ($(obj).is(":checked")) {
	        var group = "input:checkbox[name='" + $(obj).attr("name") + "']";
	        $(group).prop("checked", false);
	        $(obj).prop("checked", true);
	    } 
	  else {
	        $(obj).prop("checked", false);
	    }
}

$(document).ready(function() {
	  $(".zabbix_server").click(function() {
		  choose_one_checkbox(this);
	  });
	  $(".elk_server").click(function() {
		  choose_one_checkbox(this);
	  });
});

$(document).ready(function() {
	$("#haForm").bootstrapValidator({
		message: 'This value is not valid',
		feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
	      fields: {
	    	  keepalived_vip: {
	    		  validators: {
	    			  notEmpty: {
	                      message: 'VIP需要填写'
	                  },
	    			  ip: {
	    				  message: '请输入一个合法的VIP'
	    			  		}
	    		  		}
	    	  		},
	    	 keepalived_vip_interface: {
        		validators: {
	    			  notEmpty: {
	                      message: 'VIP网卡需要填写'
	                  },
	                  regexp: {
	                        regexp: /^[a-zA-Z0-9\.]+$/,
	                        message: '请输入一个合法的网卡名'
	                    }
	    		  	}
        		},
	    	  keepalived_vrid: {
	    		  validators: {
	    			  notEmpty: {
	                      message: '虚拟路由id需要填写,且必须为整型'
	                  },
	    			  between: {
	                        min: 1,
	                        max: 255,
	                        message: '虚拟路由id应介于1和255之间'
	                    }
	    		  }	
	    	  	}
	      	}
		});
	
	$("#addminionForm").bootstrapValidator({
		message: 'This value is not valid',
		feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
	      fields: {
	    	  
	    	  username: {
	    		  validators: {
	    			  notEmpty: {
	                      message: 'root用户名需要填写'
	                  },
	    		  	}
	    	  	},
	    	  password: {
	    		  validators: {
	    			  notEmpty: {
	                      message: 'root用户密码需要填写'
	                  },
	    		  	}
	    	  	},
	    	  yum_url: {
	    		  validators: {
	    			  notEmpty: {
	                      message: 'yum源地址需要填写'
	                  },
	                  regexp: {
	                	  regexp: "^(https|http|ftp|rtsp|mms)://"  
                		        + "?(([0-9A-z_!~*'().&=+$%-]+: )?[0-9A-z_!~*'().&=+$%-]+@)?"  
                		        + "(([0-9]{1,3}\.){3}[0-9]{1,3}"  
                		        + "|" 
                		        + "([0-9A-z_!~*'()-]+\.)*"  
                		        + "([0-9A-z][0-9A-z-]{0,61})?[0-9A-z]\."  
                		        + "[A-z]{2,6})"  
                				+ "(:[0-9]{1,4})?"  
                		        + "((/?)|"
                		        + "(/[0-9A-z_!~*'().;?:@&=+$,%#-]+)+/?)$",
                		  message: '请输入一个合法的url地址'
  	    			  		}
	    		  		}
	    	  		},
	    	  pip_url: {
	  	    		validators: {
	  	    			  notEmpty: {
	  	                      message: 'pip源地址需要填写'
	  	                  },
	  	                  regexp: {
	  	                	  regexp: "^(https|http|ftp|rtsp|mms)://"  
                		        + "?(([0-9A-z_!~*'().&=+$%-]+: )?[0-9A-z_!~*'().&=+$%-]+@)?"  
                		        + "(([0-9]{1,3}\.){3}[0-9]{1,3}"  
                		        + "|" 
                		        + "([0-9A-z_!~*'()-]+\.)*"  
                		        + "([0-9A-z][0-9A-z-]{0,61})?[0-9A-z]\."  
                		        + "[A-z]{2,6})"  
                				+ "(:[0-9]{1,4})?"  
                		        + "((/?)|"
                		        + "(/[0-9A-z_!~*'().;?:@&=+$,%#-]+)+/?)$",
                		      message: '请输入一个合法的url地址'
	  	    			  		}
	  	    		  		}
	  	    	  		},
	      },
	});
	
	
	$("#neutronForm").bootstrapValidator({
		message: 'This value is not valid',
		feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
        	vlan_start: {
        		 validators: {
	    			  notEmpty: {
	                      message: '开始vlan id需要填写'
	                  },
	    			  between: {
	                        min: 1,
	                        max: 4094,
	                        message: '起始vlan id应介于1和4094之间'
	                    }
	    		  }	
        	},
        	vlan_end: {
       		 	validators: {
	    			  notEmpty: {
	                      message: '结束vlan id需要填写'
	                  },
	    			  between: {
	                        min: 1,
	                        max: 4094,
	                        message: '结束vlan id应介于1和4094之间'
	                    }
	    		  }	
        	},
        	vxlan_start: {
       		 	validators: {
	    			  notEmpty: {
	                      message: '起始vxlan id需要填写,且必须为整型'
	                  },
	                  greaterThan: {
	                        value: 1,
	                        message: 'vxlan id应大于1'
	                    }
	    		  }	
        	},
        	vxlan_end: {
       		 	validators: {
	    			  notEmpty: {
	                      message: '结束vxlan id需要填写,且必须为整型'
	                  },
	                  greaterThan: {
	                        value: 1,
	                        message: 'vxlan id应大于1'
	                    }
	    		  }	
        	},
        	manage_interface: {
       		 	validators: {
	    			  notEmpty: {
	                      message: '管理网网卡需要填写'
	                  },
	                  regexp: {
	                        regexp: /^[a-zA-Z0-9\.]+$/,
	                        message: '请输入一个合法的网卡名'
	                  },
	                  callback: {
                          message: '不能与其它网络共用',
                          callback: function(value, validator) {
                        	  var p_int = validator.getFieldElements('public_interface').val();
                    		  var d_int = validator.getFieldElements('data_interface').val();
                    		  var m_int = validator.getFieldElements('manage_interface').val();
                        	  if ($(".neutron_vlan").is(":checked")) {
                        		  return (m_int == '' || m_int != d_int && m_int != p_int);
                        	  }
                        	  else if ($(".neutron_vxlan").is(":checked")) {
                        		  return (m_int == '' || m_int != p_int)
                        	  }
                          }
	                 } 
	    		  }	
        	},
        	storage_interface: {
       		 	validators: {
	    			  notEmpty: {
	                      message: '存储网网卡需要填写'
	                  },
	                  regexp: {
	                        regexp: /^[a-zA-Z0-9\.]+$/,
	                        message: '请输入一个合法的网卡名'
	                  },
	                  callback: {
                          message: '不能与其它网络共用',
                          callback: function(value, validator) {
                        	  var p_int = validator.getFieldElements('public_interface').val();
                    		  var d_int = validator.getFieldElements('data_interface').val();
                    		  var s_int = validator.getFieldElements('storage_interface').val();
                        	  if ($(".neutron_vlan").is(":checked")) {
                        		  return (s_int == '' || s_int != d_int && s_int != p_int);
                        	  }
                        	  else if ($(".neutron_vxlan").is(":checked")) {
                        		  return (s_int == '' || s_int != p_int)
                        	  }
                          }
	                 } 
	    		  }	
        	},
        	storage_cidr: {
       		 	validators: {
	    			  notEmpty: {
	                      message: '存储网网络地址需要填写'
	                  },
	                  regexp: {
	                        regexp: /^(([1-9]|([1-9]\d)|(1\d\d)|(2([0-4]\d|5[0-5])))\.)(([0-9]|([0-9]\d)|(1\d\d)|(2([0-4]\d|5[0-5])))\.){2}0\/24$/,    
	                        message: '请输入一个合法的cidr'
	                    }
	    		  }	
        	},
        	data_interface: {
       		 	validators: {
	    			  notEmpty: {
	                      message: '虚拟机业务网网卡需要填写'
	                  },
	                  regexp: {
	                        regexp: /^[a-zA-Z0-9\.]+$/,
	                        message: '请输入一个合法的网卡名'
	                  },
	                  callback: {
                          message: '虚拟机业务网络不能与其它网络共用',
                          callback: function(value, validator) {
                        	  var p_int = validator.getFieldElements('public_interface').val();
                    		  var d_int = validator.getFieldElements('data_interface').val();
                    		  var s_int = validator.getFieldElements('storage_interface').val();
                    		  var m_int = validator.getFieldElements('manage_interface').val();
                        	  if ($(".neutron_vlan").is(":checked")) {
                        		  return (d_int == '' || d_int != p_int && d_int != s_int && d_int != m_int);
                        	  }
                        	  else if ($(".neutron_vxlan").is(":checked")) {
                        		  return (d_int == '' || d_int != p_int)
                        	  }
                          }
	                 } 
	    		  }	
        	},
        	public_interface: {
       		 	validators: {
	    			  notEmpty: {
	                      	message: '虚拟机浮动ip网网卡需要填写'
	                  },
	                  regexp: {
	                        regexp: /^[a-zA-Z0-9\.]+$/,
	                        message: '请输入一个合法的网卡名'
	                    },
	                  callback: {
                            message: '虚拟机浮动ip网络不能与其它网络共用',
                            callback: function(value, validator) {
                                var p_int = validator.getFieldElements('public_interface').val();
                                var d_int = validator.getFieldElements('data_interface').val();
                                var s_int = validator.getFieldElements('storage_interface').val();
                                var m_int = validator.getFieldElements('manage_interface').val();
                                return (p_int == '' || p_int != d_int && p_int != s_int && p_int != m_int);
                            }
                        },
	    		  }	
        	},
        	data_cidr: {
       		 	validators: {
	    			  notEmpty: {
	                      message: '虚拟机浮动ip网网络地址需要填写'
	                  },
	                  regexp: {
	                        regexp: /^(([1-9]|([1-9]\d)|(1\d\d)|(2([0-4]\d|5[0-5])))\.)(([0-9]|([0-9]\d)|(1\d\d)|(2([0-4]\d|5[0-5])))\.){2}0\/24$/,    
	                        message: '请输入一个合法的cidr'
	                    }
	    		  }	
        	},
        }
	});
});

function isAddOk() {
	$( document ).ready(function() {
		$('#result').html("");
//      var master = $("input[name='master']").val();
        var username = $("input[name='username']").val();
        var password = $("input[name='password']").val();
        var yum_url = $("input[name='yum_url']").val();
        var pip_url = $("input[name='pip_url']").val();
//        var private_key = $("#private_key").val();
//        var fileInput = $("#ssh_key");
        var fileInput = document.getElementById("ssh_key");
        var private_key = '';
       
        if (window.File && window.FileReader && window.FileList && window.Blob) {
        	console.log("Great success! All the File APIs are supported.");
			} 
		else {
			 alert('The File APIs are not fully supported in this browser.');
			}
        
        var reader = new FileReader();
        if (fileInput.files.length > 0) {
        	reader.readAsText(fileInput.files[0]);
        	reader.onload = function(evt){
        		private_key = evt.target.result;
        		$.post(
        	    		 "/salt/upload/",
        	    		 {
        	    			'private_key': private_key,
        	    		 }, function(ret){
        	    			 return true;
        	    		 },
        	 	        "json"
        	 	     )
        	    }
        	};
        
		var compute_minions = "";
		var compute_minions_list = $('input[name="minions_ip"]:checked');
		 jQuery.each(compute_minions_list, function(i, v){
			 
			 if (i != compute_minions_list.length-1) {
				 compute_minions += $(v).val() + ','; 
			 }
			 else {
				 compute_minions += $(v).val();
			 }
		 });
		 
		 if (compute_minions === "" || compute_minions === null) {
		     alert("没有任何要添加的minion节点！");
		     return false;
		  }
	     if (username === '' || username === null) {
	        	alert('请输入root用户名');
	        	return false;
	        }
	     if (yum_url === '' || yum_url === null) {
	        	alert('请输入yum本地源地址');
	        	return false;
	        }
	     if (pip_url === '' || pip_url === null) {
	        	alert('请输入pip本地源地址');
	        	return false;
	        }
	     
	     $("#execapi").attr("disabled","disabled");
	     $("#execapi").html('<img src="/static/img/button.gif" style="width:28px;height:16px;"/>');
	     $.post(
	    		 "/salt/add/",
	    		 {
	    			 'minions': compute_minions,
	    			 'username': username,
	    			 'password': password,
	    			 'yum_url': yum_url,
	    			 'pip_url': pip_url,
	    		 }, function(ret){
	            if (ret.hasOwnProperty('errors')) {
	                alert(ret.errors);
	                $("#execapi").removeAttr("disabled");
	                $("#execapi").html("添加");
	                return false;
	            } else {
	                if (ret.add_res===0) {
	                    $('#result').html('\
	                    <div class="alert alert-success fade in">\
	    					<a href="#" class="close" data-dismiss="alert">&times;</a>\
	    					<strong>Success!</strong> 添加成功，请查看左边MinionsKeys面板\
	    				</div>'
	                    );
	                } 
	                
	                else if (ret.add_res===1) {
	                    $('#result').html('\
	    	                <div class="alert alert-danger fade in">\
	    	    				<a href="#" class="close" data-dismiss="alert">&times;</a>\
	    	    				<strong>Error!</strong> 添加失败\
	    	    			</div>'
	    	             );
	                }
	            };
	            $("#execapi").removeAttr("disabled");
	            $("#execapi").html("添加");
	        },
	        "json"
	     )
    })
}


function addOpsConfig() {
	$(document).ready(function(){
		var compute_minions = "";
		var compute_minions_list = $('input[name="compute_minions"]:checked');
		
		var config_zabbix_install = 'false';
		var config_elk_install = 'false';
		var config_storage_install = "false";
		var storage_osd_minions = "";
		var zabbix_agent_minions = "";
		var elk_agent_minions = "";
		var zabbix_agent_minions_list = $('input[name="zabbix_agent_minions"]:checked');
		var elk_agent_minions_list = $('input[name="elk_agent_minions"]:checked');
		
		var nova_storage_backends = $('input[name="nova_storage"]:checked').val();
		
		var enable_distri_storage = $('input[name="enable_distri_storage"]');
		var ceph_osd_minions_list = $('input[name="ceph_osd_minions"]:checked');
		var ceph_osd_devs = {};
		
		var enable_monitor = $('input[name="enable_monitor"]');
		var enable_elk = $('input[name="enable_elk"]');
		
		if ($(enable_distri_storage).is(":checked")) {
			config_storage_install = 'true';
		}
		else {
			config_storage_install = 'false';
		}
		
		/*
		 * 对是否启用监控、elk的条件判断
		 */
		if ($(enable_monitor).is(":checked")) {
			config_zabbix_install = 'true';
		}
		else {
			config_zabbix_install = 'false';
		}
		
		if ($(enable_elk).is(":checked")) {
			config_elk_install = 'true';
		}
		else {
			config_elk_install = 'false';
		}
		
		/*
		 * 获取所选的所有计算节点salt agent
		 */
		 jQuery.each(compute_minions_list, function(i, v){
			 
			 if (i != compute_minions_list.length-1) {
				 compute_minions += $(v).val() + ','; 
			 }
			 else {
				 compute_minions += $(v).val();
			 }
		 });
		 
		 if (compute_minions === "" || compute_minions === null) {
		     alert("未选择任何compute节点！");
		     return false;
		  }
		 
		 jQuery.each(zabbix_agent_minions_list, function(i, v){
			 if (i != zabbix_agent_minions_list.length-1) {
				 zabbix_agent_minions += $(v).val() + ','; 
			 }
			 else {
				 zabbix_agent_minions += $(v).val();
			 }
		 });
		 
		 jQuery.each(elk_agent_minions_list, function(i, v){
			 if (i != elk_agent_minions_list.length-1) {
				 elk_agent_minions += $(v).val() + ','; 
			 }
			 else {
				 elk_agent_minions += $(v).val();
			 }
		 });
		 
		 var osd_err = 0;
		 jQuery.each(ceph_osd_minions_list, function(i, v){
				
				var ceph_osd_minion = $(v).val();
				var osd_devs = "";
				
				var ceph_osd_devs_list = $('input[name=' + ceph_osd_minion + '_osds]:checked');
				if (ceph_osd_devs_list.length == 0) {
					alert("未对osd节点" + ceph_osd_minion + "分配任何osd磁盘设备");
					osd_err = 1;
					return false;
				}
				
				jQuery.each(ceph_osd_devs_list, function(i, v){
					 if (i != ceph_osd_devs_list.length-1) {
						 osd_devs += $(v).val() + ','; 
					 }
					 else {
						 osd_devs += $(v).val();
					 }
				 });
				
				ceph_osd_devs[ceph_osd_minion + ""] = osd_devs;
				
				 if (i != ceph_osd_minions_list.length-1) {
					 storage_osd_minions += $(v).val() + ','; 
				 }
				 else {
					 storage_osd_minions += $(v).val();
				 }
			 });
		 
		 if (osd_err == 1) {
			 return false;
		 }
		 
		 $("#configapi").attr("disabled","disabled");
		 $("#configapi_rd").attr("disabled","disabled");
	     $("#configapi").html('<img src="/static/img/button.gif" style="width:28px;height:16px;"/>');
	     $("#configapi_rd").html('<img src="/static/img/button.gif" style="width:28px;height:16px;"/>');
	     $.post(
	    		 "/salt/openstack/env/add/",
	    		 {
	    			 'config_storage_install': config_storage_install,
	    			 'config_zabbix_install': config_zabbix_install,
	    			 'config_elk_install': config_elk_install,
	    			 'compute_minions': compute_minions,
	    			 'zabbix_agent_minions': zabbix_agent_minions,
	    			 'elk_agent_minions': elk_agent_minions,
	    			 'storage_osd_minions': storage_osd_minions,
	    			 'ceph_osd_devs': JSON.stringify(ceph_osd_devs),
	    			 'nova_storage_backends': nova_storage_backends,
	    		 }, function(ret){
	            if (ret.hasOwnProperty('errors')) {
	                alert(ret.errors);
	                $("#configapi").removeAttr("disabled");
	                $("#configapi_rd").removeAttr("disabled");
	                $("#configapi").html("完成");
	                $("#configapi_rd").html("完成");
	                return false;
	            } else {
	                if (ret.ret_code===0) {
	                    $('#result').html('\
	                    <div class="alert alert-success fade in">\
	    					<a href="#" class="close" data-dismiss="alert">&times;</a>\
	    					<strong>Success!</strong> 添加OpenStack节点配置成功\
	    				</div>'
	                    );
	                } 
	                
	                else if (ret.ret_code===1) {
	                    $('#result').html('\
	    	                <div class="alert alert-danger fade in">\
	    	    				<a href="#" class="close" data-dismiss="alert">&times;</a>\
	    	    				<strong>Error!</strong> 添加OpenStack节点配置失败\
	    	    			</div>'
	    	             );
	                }
	            };
	            $("#configapi").removeAttr("disabled");
	            $("#configapi_rd").removeAttr("disabled");
	            $("#configapi").html("完成");
	            $("#configapi_rd").html("完成");
	        },
	        "json"
	     )
		 
	});
}


function createOpsConfig() {
	$(document).ready(function(){
		/*
		 * ha变量定义:
		 * 1、是否启用HA
		 * 2、keepalived虚拟ip
		 * 3、keepalived虚拟路由id配置
		 */
		var enable_ha = $('input[name="enable_ha"]');
		var config_ha_install = 'false';
		var keepalived_vip = "";
		var keepalived_vrid = "";
		var keepalived_vip_interface = "";
		
		/*
		 * storage变量定义:
		 * 
		 */
		var enable_distri_storage = $('input[name="enable_distri_storage"]');
		
		/*
		 * 节点变量定义:
		 * 计算节点salt agent
		 * 控制节点salt agent
		 * 存储节点salt agent
		 */
		var compute_minions = "";
		var controller_minions = "";
		var zabbix_server_minions = "";
		var zabbix_agent_minions = "";
		var elk_server_minions = "";
		var elk_agent_minions = "";
		var storage_mon_minions = "";
		var storage_osd_minions = "";
		var config_storage_install = "false";
		var storage_backends = "file";
		var virt_type = $('input[name="virt_type"]:checked').val();
		
		var compute_minions_list = $('input[name="compute_minions"]:checked');
		var controller_minions_list = $('input[name="controller_minions"]:checked');
		var ceph_mon_minions_list = $('input[name="ceph_mon_minions"]:checked');
		var ceph_osd_minions_list = $('input[name="ceph_osd_minions"]:checked');
		var ceph_osd_devs = {};
		
		/*
		 * 网络变量定义
		 */
		var neutron_mode = $("input[name='neutron_mode']:checked").val();
		var vlan_start = "";
		var vlan_end = "";
		var vxlan_start = "";
		var vxlan_end = "";
		var manage_interface = $('input[name="manage_interface"]').val();
		var data_interface = $('input[name="data_interface"]').val();
		var storage_interface = $('input[name="storage_interface"]').val();
		var public_interface = $('input[name="public_interface"]').val();
		var storage_cidr = $('input[name="storage_cidr"]').val();
		var data_cidr = $('input[name="data_cidr"]').val();
		
		/*
		 * 监控、elk变量定义
		 */
		var enable_monitor = $('input[name="enable_monitor"]');
		var enable_elk = $('input[name="enable_elk"]');
		var config_zabbix_install = 'false';
		var config_elk_install = 'false';
		var zabbix_server_minions_list = $('input[name="zabbix_server_minions"]:checked');
		var elk_server_minions_list = $('input[name="elk_server_minions"]:checked');
		var zabbix_agent_minions_list = $('input[name="zabbix_agent_minions"]:checked');
		var elk_agent_minions_list = $('input[name="elk_agent_minions"]:checked');
		
		/*
		 * 对是否启用HA的条件判断
		 */
		if ($(enable_ha).is(":checked")) {
			config_ha_install = 'true';
			keepalived_vip = $('input[name="keepalived_vip"]').val();
			keepalived_vrid = $('input[name="keepalived_vrid"]').val();
			keepalived_vip_interface = $('input[name="keepalived_vip_interface"]').val();
			
			/*
			 * 控制节点HA目前只支持1个或3个节点
			 */
			var con_minions_len = controller_minions_list.length
			if (con_minions_len != 1 && con_minions_len !=3) {
				alert("控制节点高可用只支持1个或3个节点");
				return false;
			}
			console.log("enable ha");
		}
		else {
			console.log("not enable ha");
		}
		
		console.log(neutron_mode);
		
		/*
		 * 对是否启用监控、elk的条件判断
		 */
		if ($(enable_monitor).is(":checked")) {
			config_zabbix_install = 'true';
		}
		else {
			config_zabbix_install = 'false';
		}
		
		if ($(enable_elk).is(":checked")) {
			config_elk_install = 'true';
		}
		else {
			config_elk_install = 'false';
		}
		
		
		var osd_err = 0;
		/*
		 * 对是否启用分布式存储的判断
		 */
		if ($(enable_distri_storage).is(":checked")) {
			config_storage_install = 'true';
			storage_backends = $('input[name="storage"]:checked').val();
			console.info(storage_backends);
			if (storage_backends === 'ceph'){
				var mon_minions_len = ceph_mon_minions_list.length;
				console.info("enable ceph");
				if (mon_minions_len %2 != 1) {
					alert("ceph集群monitor节点数量必须为奇数");
					return false;
				}
				
				/*
				 * 获取所选的所有ceph节点salt agent
				 */
				jQuery.each(ceph_mon_minions_list, function(i, v){
					 if (i != ceph_mon_minions_list.length-1) {
						 storage_mon_minions += $(v).val() + ','; 
					 }
					 else {
						 storage_mon_minions += $(v).val();
					 }
				 });
				
				jQuery.each(ceph_osd_minions_list, function(i, v){
						
					var ceph_osd_minion = $(v).val();
					var osd_devs = "";
					
					var ceph_osd_devs_list = $('input[name=' + ceph_osd_minion + '_osds]:checked');
					if (ceph_osd_devs_list.length == 0) {
						alert("未对osd节点" + ceph_osd_minion + "分配任何osd磁盘设备");
						osd_err = 1;
						return false;
					}
					
					jQuery.each(ceph_osd_devs_list, function(i, v){
						 if (i != ceph_osd_devs_list.length-1) {
							 osd_devs += $(v).val() + ','; 
						 }
						 else {
							 osd_devs += $(v).val();
						 }
					 });
					
					ceph_osd_devs[ceph_osd_minion + ""] = osd_devs;
					
					 if (i != ceph_osd_minions_list.length-1) {
						 storage_osd_minions += $(v).val() + ','; 
					 }
					 else {
						 storage_osd_minions += $(v).val();
					 }
				 });
				
			}
		}
		else {
			config_storage_install = 'false';
		}
		
		 console.info(ceph_osd_devs, storage_mon_minions, storage_osd_minions);
		
		/*
		 * 获取所选的所有计算节点salt agent
		 */
		 jQuery.each(compute_minions_list, function(i, v){
			 
			 if (i != compute_minions_list.length-1) {
				 compute_minions += $(v).val() + ','; 
			 }
			 else {
				 compute_minions += $(v).val();
			 }
		 });
		 
		 if (compute_minions === "" || compute_minions === null) {
		     alert("未选择任何compute节点！");
		     return false;
		  }
		 
		 /*
		  * 获取所选的所有控制节点salt agent
		  */
		 jQuery.each(controller_minions_list, function(i, v){
			 
			 if (i != controller_minions_list.length-1) {
				 controller_minions += $(v).val() + ','; 
			 }
			 else {
				 controller_minions += $(v).val();
			 }
		 });
		 
		 if (controller_minions === "" || controller_minions === null) {
		     alert("未选择任何controller节点！");
		     return false;
		  }
		 
		 /*
		  * 获取所选的所有zabbix节点salt agent
		  */
		 jQuery.each(zabbix_server_minions_list, function(i, v){
			 
			 if (i != zabbix_server_minions_list.length-1) {
				 zabbix_server_minions += $(v).val() + ','; 
			 }
			 else {
				 zabbix_server_minions += $(v).val();
			 }
		 });
		 
		 jQuery.each(zabbix_agent_minions_list, function(i, v){
			 
			 if (i != zabbix_agent_minions_list.length-1) {
				 zabbix_agent_minions += $(v).val() + ','; 
			 }
			 else {
				 zabbix_agent_minions += $(v).val();
			 }
		 });
		 
		 /*
		  * 获取所选的所有elk节点salt agent
		  */
		 jQuery.each(elk_server_minions_list, function(i, v){
			 
			 if (i != elk_server_minions_list.length-1) {
				 elk_server_minions += $(v).val() + ','; 
			 }
			 else {
				 elk_server_minions += $(v).val();
			 }
		 });
		 
		 jQuery.each(elk_agent_minions_list, function(i, v){
			 
			 if (i != elk_agent_minions_list.length-1) {
				 elk_agent_minions += $(v).val() + ','; 
			 }
			 else {
				 elk_agent_minions += $(v).val();
			 }
		 });
		 
		 
		 /*
		  * 获取部署网络配置信息
		  */
		 if (neutron_mode === 'vlan') {
				vlan_start = $('input[name="vlan_start"]').val();
				vlan_end = $('input[name="vlan_end"]').val();
			}
		 else if (neutron_mode === 'vxlan') {
				vxlan_start = $('input[name="vxlan_start"]').val();
				vxlan_end = $('input[name="vxlan_end"]').val();
		 	}
		 
		 if (osd_err == 1) {
			 return false;
		 }
		 
		 $("#configapi").attr("disabled","disabled");
		 $("#configapi_rd").attr("disabled","disabled");
	     $("#configapi").html('<img src="/static/img/button.gif" style="width:28px;height:16px;"/>');
	     $("#configapi_rd").html('<img src="/static/img/button.gif" style="width:28px;height:16px;"/>');
	     $.post(
	    		 "/salt/openstack/env/create/",
	    		 {
	    			 'config_ha_install': config_ha_install,
	    			 'config_storage_install': config_storage_install,
	    			 'config_zabbix_install': config_zabbix_install,
	    			 'config_elk_install': config_elk_install,
	    			 'keepalived_vip': keepalived_vip,
	    			 'keepalived_vrid': keepalived_vrid,
	    			 'keepalived_vip_interface': keepalived_vip_interface,
	    			 'controller_minions': controller_minions,
	    			 'compute_minions': compute_minions,
	    			 'virt_type': virt_type,
	    			 'zabbix_server_minions': zabbix_server_minions,
	    			 'zabbix_agent_minions': zabbix_agent_minions,
	    			 'elk_server_minions': elk_server_minions,
	    			 'elk_agent_minions': elk_agent_minions,
	    			 'storage_mon_minions': storage_mon_minions,
	    			 'storage_osd_minions': storage_osd_minions,
	    			 'storage_backends': storage_backends,
	    			 'ceph_osd_devs': JSON.stringify(ceph_osd_devs),
	    			 'neutron_mode': neutron_mode,
	    			 'vlan_start': vlan_start,
	    			 'vlan_end': vlan_end,
	    			 'vxlan_start': vxlan_start,
	    			 'vxlan_end': vxlan_end,
	    			 'manage_interface': manage_interface,
	    			 'data_interface': data_interface,
	    			 'storage_interface': storage_interface,
	    			 'public_interface': public_interface,
	    			 'storage_cidr': storage_cidr,
	    			 'data_cidr': data_cidr
	    		 }, function(ret){
	            if (ret.hasOwnProperty('errors')) {
	                alert(ret.errors);
	                $("#configapi").removeAttr("disabled");
	                $("#configapi_rd").removeAttr("disabled");
	                $("#configapi").html("完成");
	                $("#configapi_rd").html("完成");
	                return false;
	            } else {
	                if (ret.ret_code===0) {
	                    $('#result').html('\
	                    <div class="alert alert-success fade in">\
	    					<a href="#" class="close" data-dismiss="alert">&times;</a>\
	    					<strong>Success!</strong> 初始化OpenStack环境配置成功\
	    				</div>'
	                    );
	                } 
	                
	                else if (ret.ret_code===1) {
	                    $('#result').html('\
	    	                <div class="alert alert-danger fade in">\
	    	    				<a href="#" class="close" data-dismiss="alert">&times;</a>\
	    	    				<strong>Error!</strong> 初始化OpenStack环境配置失败\
	    	    			</div>'
	    	             );
	                }
	            };
	            $("#configapi").removeAttr("disabled");
	            $("#configapi_rd").removeAttr("disabled");
	            $("#configapi").html("完成");
	            $("#configapi_rd").html("完成");
	        },
	        "json"
	     )
	});
}


function installOpenStack() {
	$( document ).ready(function() {
		 $('#result').html("");
		 $('#info').html("");
		
	     $("#deployos").attr("disabled","disabled");
	     $("#deployos").html('<img src="/static/img/button.gif" style="width:28px;height:16px;"/>');
	     $.post(
	    		 "/salt/openstack/api/deploy/",
	    		 {
	    		 }, function(ret){
	            if (ret.hasOwnProperty('errors')) {
	                alert(ret.errors);
	                $("#deployos").removeAttr("disabled");
	                $("#deployos").html("开始安装");
	                return false;
	            } else {
	                if (ret.ret_code===0) {
	                	
	                    $('#result').html('\
	                    <div class="alert alert-success fade in">\
	    					<a href="#" class="close" data-dismiss="alert">&times;</a>\
	    					<strong>Success!</strong> 安装程序正在进行中,请查看安装log......\
	    				</div>'
	                    	);
	                } 
	                else if (ret.ret_code===1) {
	                    $('#result').html('\
	    	                <div class="alert alert-danger fade in">\
	    	    				<a href="#" class="close" data-dismiss="alert">&times;</a>\
	    	    				<strong>Error!</strong> 操作失败\
	    	    			</div>'
	    	             );
	                }
	                else if (ret.ret_code===2) {
	                    $('#result').html('\
	    	                <div class="alert alert-warning fade in">\
	    	    				<a href="#" class="close" data-dismiss="alert">&times;</a>\
	    	    				<strong>Warning!</strong> 安装程序已经在运行中，请查看安装log......\
	    	    			</div>'
	    	             );
	                }
	            };
	            $("#deployos").removeAttr("disabled");
	            $("#deployos").html("开始安装");
	        },
	        "json"
	     )
    })
}


function addOpenStack() {
	$( document ).ready(function() {
		 $('#result').html("");
		 $('#info').html("");
		
	     $("#deployos").attr("disabled","disabled");
	     $("#deployos").html('<img src="/static/img/button.gif" style="width:28px;height:16px;"/>');
	     $.post(
	    		 "/salt/openstack/api/add/",
	    		 {
	    		 }, function(ret){
	            if (ret.hasOwnProperty('errors')) {
	                alert(ret.errors);
	                $("#deployos").removeAttr("disabled");
	                $("#deployos").html("开始扩容");
	                return false;
	            } else {
	                if (ret.ret_code===0) {
	                	
	                    $('#result').html('\
	                    <div class="alert alert-success fade in">\
	    					<a href="#" class="close" data-dismiss="alert">&times;</a>\
	    					<strong>Success!</strong> 扩容程序正在进行中,请查看扩容log......\
	    				</div>'
	                    	);
	                } 
	                else if (ret.ret_code===1) {
	                    $('#result').html('\
	    	                <div class="alert alert-danger fade in">\
	    	    				<a href="#" class="close" data-dismiss="alert">&times;</a>\
	    	    				<strong>Error!</strong> 操作失败\
	    	    			</div>'
	    	             );
	                }
	                else if (ret.ret_code===2) {
	                    $('#result').html('\
	    	                <div class="alert alert-warning fade in">\
	    	    				<a href="#" class="close" data-dismiss="alert">&times;</a>\
	    	    				<strong>Warning!</strong> 扩容程序已经在运行中，请查看扩容log......\
	    	    			</div>'
	    	             );
	                }
	            };
	            $("#deployos").removeAttr("disabled");
	            $("#deployos").html("开始扩容");
	        },
	        "json"
	     )
    })
}

function checkInsPro() {
	$( document ).ready(function() {
		var strip_bar = '';
		$.getJSON("/salt/openstack/api/check_deploy_process/", function(ret){
			if (ret.res===2) {
                $('#result').html('\
	                <div class="alert alert-warning fade in">\
	    				<a href="#" class="close" data-dismiss="alert">&times;</a>\
	    				<strong>Warning!</strong> 安装程序未运行\
	    			</div>'
	           );
			}
			else if (ret.res===1) {
				if (ret.process_percent == 100) {
					strip_bar = '';
					window.clearTimeout(chkInsPro_id);
				}
				else {
					strip_bar = 'progress-bar-striped active';
				}
				$('#result').html('\
					<div class="control-group">\
						<label class="controls">安装进度</label>\
						<div class="progress">\
                		<div class="progress-bar ' + strip_bar + '" role="progressbar" aria-valuenow="' + ret.process_percent + '" aria-valuemin="0" aria-valuemax="100"\
                		style="width:' + ret.process_percent + '%">' + ret.process_percent + '%</div>\
                  		</div>\
                    	<label class="controls">执行过程</label>\
                        	<div class="controls">' + ret.content + '</div>\
                	</div>');
			}
		})
               var chkInsPro_id = window.setTimeout("checkInsPro()", 5000);
	})
}

function saltFunc() {
    //$.ajaxSettings.async = false;
    $(document).ready(function(){
        $("#info").html("");
        $("#result").html("");
        var tgt = $("input[name='tgt']").val();
        var datacenter = "";
        var arg = "";
        $("input[name='datacenter']:checked").each(function(){
            datacenter += $(this).val() + ',';
        });
        $("input[name='sls']:checked").each(function(){
            arg = $(this).val();
        });
        if ((tgt === '' || tgt === null) && (datacenter === '' || datacenter === null)) {
            alert('请输入服务器IP或选择对应机房！');
            return false;
        };
        if (arg === '' || arg === null) {
            alert('请选择将要进行的操作！');
            return false;
        };
        $("#salt_submit").attr("disabled","disabled");
        $("#salt_submit").html('<img src="/static/img/button.gif" style="width:28px;height:16px;"/>');
        $.getJSON("/salt/api/deploy/", {"tgt":tgt, "datacenter":datacenter, "sls":arg}, function(ret){
            if (ret.hasOwnProperty("errors")) {
                alert(ret.errors);
                $("#salt_submit").removeAttr("disabled");
                $("#salt_submit").html("提交");
                return false;
            } else {
                if (ret.info.unrecv_count === 0) {
                    $("#info").html('\
                        <hr/>本次执行对象'+ret.info.send_count+'台，\
                        共'+ret.info.recv_count+'台返回结果，\
                        其中成功'+ret.info.succeed+'台，\
                        失败'+ret.info.failed+'台；<hr/>'
                    );
                } else {
                    $("#info").html('\
                        <hr/>本次执行对象'+ret.info.send_count+'台，\
                        共'+ret.info.recv_count+'台返回结果，\
                        其中成功'+ret.info.succeed+'台，\
                        失败'+ret.info.failed+'台；\
                        未返回结果的有以下'+ret.info.unrecv_count+'台:\
                        <br/>'+ ret.info.unrecv_strings+';<hr/>'
                    );
                }
            }
            var sortArray = [];
            $.each(ret.result, function(key, value) {
                sortArray[sortArray.length] = key;
            });
            sortArray.sort();
            $.each(sortArray, function(i, key) {
                var ip_nodot = key.replace(/\./g,'');
                if (ret['result'][key]['status'] === 'True') {
                    $("#result").append('\
                        <div class="col-md-3" style="margin-bottom:5px">\
                            <button type="button" class="btn btn-info btn-block" data-toggle="modal" data-target="#'+ip_nodot+'">'+key+'</button>\
                        </div>\
                        <div class="modal fade bs-example-modal-lg" id="'+ip_nodot+'" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\
                          <div class="modal-dialog modal-lg">\
                            <div class="modal-content">\
                              <div class="modal-header">\
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>\
                                <h4 class="modal-title" id="myModalLabel">'+key+'</h4>\
                              </div>\
                              <div class="modal-body">\
                                <pre>'+ret['result'][key]['cont']+'</pre>\
                              </div>\
                              <div class="modal-footer">\
                                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>\
                              </div>\
                            </div>\
                          </div>\
                        </div>'
                    );
                } else {
                    $("#result").append('\
                        <div class="col-md-3" style="margin-bottom:5px">\
                            <button type="button" class="btn btn-danger btn-block" data-toggle="modal" data-target="#'+ip_nodot+'">'+key+'</button>\
                        </div>\
                        <div class="modal fade bs-example-modal-lg" id="'+ip_nodot+'" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\
                          <div class="modal-dialog modal-lg">\
                            <div class="modal-content">\
                              <div class="modal-header">\
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>\
                                <h4 class="modal-title" id="myModalLabel">'+key+'</h4>\
                              </div>\
                              <div class="modal-body">\
                                <pre>'+ret['result'][key]['cont']+'</pre>\
                              </div>\
                              <div class="modal-footer">\
                                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>\
                              </div>\
                            </div>\
                          </div>\
                        </div>');
                };
            });
            $("#salt_submit").removeAttr("disabled");
            $("#salt_submit").html("提交");
        });
    });
    //$.ajaxSettings.async = true;
}

//修复历史数据
function repairHistoryData() {
    $("#info").html("");
    $("#result").html("");
    var datacenter = "";
    var stockexchange = "";
    var sls = "";
    $("input[name='datacenter']:checked").each(function(){
        datacenter += $(this).val() + ',';
    });
    $("input[name='stockexchange']:checked").each(function(){
        stockexchange += $(this).val() + ',';
    });
    $("input[name='sls']:checked").each(function(){
        sls = $(this).val();
    });
    if (datacenter === '' || datacenter === null) {
        alert('请选择将要操作的机房！');
        return false;
    }
    if (stockexchange === '' || stockexchange === null) {
        alert('请选择将要补数据的市场！');
        return false;
    }
    if (sls === '' || sls === null) {
        alert('请选择补过数据以后是否需要重启行情程序！');
        return false;
    }
    $("#submit_history").attr("disabled","disabled");
    $("#submit_history").html('<img src="/static/img/button.gif" style="width:28px;height:16px;"/>');
    $.getJSON("/data/api/history/", {"datacenter":datacenter, "stockexchange":stockexchange, "sls": sls}, function(ret){
        if (ret.hasOwnProperty("errors")) {
            alert(ret.errors);
            $("#submit_history").removeAttr("disabled");
            $("#submit_history").html("提交");
            return false;
        } else {
            if (ret.info.unrecv_count === 0) {
                $("#info").html('\
                    <hr/>本次执行对象'+ret.info.send_count+'台，\
                    共'+ret.info.recv_count+'台返回结果，\
                    其中成功'+ret.info.succeed+'台，\
                    失败'+ret.info.failed+'台；<hr/>'
                );
            } else {
                $("#info").html('\
                    <hr/>本次执行对象'+ret.info.send_count+'台，\
                    共'+ret.info.recv_count+'台返回结果，\
                    其中成功'+ret.info.succeed+'台，\
                    失败'+ret.info.failed+'台；\
                    未返回结果的有以下'+ret.info.unrecv_count+'台:\
                    <br/>'+ ret.info.unrecv_strings+'<hr/>'
                );
            }
        }
        var sortArray = [];
        $.each(ret.result, function(key, value) {
            sortArray[sortArray.length] = key;
        });
        sortArray.sort();
        $.each(sortArray, function(i, key) {
            var ip_nodot = key.replace(/\./g,'');
            if (ret['result'][key]['status'] === 'True') {
                $("#result").append('\
                    <div class="col-md-3" style="margin-bottom:5px">\
                        <button type="button" class="btn btn-info btn-block" data-toggle="modal" data-target="#'+ip_nodot+'">'+key+'</button>\
                    </div>\
                    <div class="modal fade bs-example-modal-lg" id="'+ip_nodot+'" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\
                      <div class="modal-dialog modal-lg">\
                        <div class="modal-content">\
                          <div class="modal-header">\
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>\
                            <h4 class="modal-title" id="myModalLabel">'+key+'</h4>\
                          </div>\
                          <div class="modal-body">\
                            <pre>'+ret['result'][key]['cont']+'</pre>\
                          </div>\
                          <div class="modal-footer">\
                            <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>\
                          </div>\
                        </div>\
                      </div>\
                    </div>'
                );
            } else {
                $("#result").append('\
                    <div class="col-md-3" style="margin-bottom:5px">\
                        <button type="button" class="btn btn-danger btn-block" data-toggle="modal" data-target="#'+ip_nodot+'">'+key+'</button>\
                    </div>\
                    <div class="modal fade bs-example-modal-lg" id="'+ip_nodot+'" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\
                      <div class="modal-dialog modal-lg">\
                        <div class="modal-content">\
                          <div class="modal-header">\
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>\
                            <h4 class="modal-title" id="myModalLabel">'+key+'</h4>\
                          </div>\
                          <div class="modal-body">\
                            <pre>'+ret['result'][key]['cont']+'</pre>\
                          </div>\
                          <div class="modal-footer">\
                            <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>\
                          </div>\
                        </div>\
                      </div>\
                    </div>');
            };
        });
        $("#submit_history").removeAttr("disabled");
        $("#submit_history").html("提交");
    });
}
