<?php

class Validate{
	private $_passed = false,
			$_errors = array(),
			$_db = null;
			
	public function __construct(){
		$this->_db = DB::getInstance();
	}
	
	public function check($source, $items = array()){
		foreach($items as $item => $rules){
			foreach($rules as $rule => $rule_value){
				
				$value = trim($source[$item]);
				$item = escape($item);
				
				if($rule === 'required' & empty($value)){
					$this->addError("{$item} é necessário");
				}else if(!empty($value)){
					switch($rule){
						case 'min':
							if(strlen($value) < $rule_value){
								$this->addError("{$item} precisa ter um mínimo de {$rule_value} caracteres.");
							}
						break;
						
						case 'max':
							if(strlen($value) > $rule_value){
								$this->addError("{$item} precisa ter um máximo de {$rule_value} caracteres.");
							}
						break;
						
						case 'matches':
							if($value != $source[$rule_value]){
								$this->addError("{$rule_value} must match {$item}");
							}
						break;
						
						case 'unique':
							$check = $this->_db->get($rule_value, array($item, '=', $value));
							if($check->count()){
								$this->addError("{$item} já existe.");
							}
						break;
					}
				}
				
			}
		}
		
		if(empty($this->_errors)){
			$this->_passed = true;
		}
		
		return $this;
	}
	
	public function addError($error){
		$this->_errors[] = $error;
	}
	
	public function errors(){
		return $this->_errors;
	}
	
	public function passed(){
		return $this->_passed;
	}
}