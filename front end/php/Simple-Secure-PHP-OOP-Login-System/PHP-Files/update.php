<?php
require_once 'core/init.php';

$user = new User();

if(!$user->isLoggedIn()){
	Redirect::to('index.php');
}

if(Input::exists()){
	if(Token::check(Input::get('token'))){
		
		$validate = new Validate();
		$validation = $validate->check($_POST, array(
			'name' => array(
				'required' => true,
				'min' => 2,
				'max' => 50
			)
		));
		
		if($validation->passed()){
			
			try{
				$user->update(array(
					'name' => Input::get('name')
				));
				
				Session::flash('home', 'Suas informações foram atualizadas.');
				Redirect::to('index.php');
				
			}catch(Exception $e){
				die($e->getMessage());
			}
			
		}else{
			foreach($validation->errors() as $error){
				echo $error, '<br>';
			}
		}
		
	}
}

?>

<form action="" method="post">
	<div class="field">
		<label for="name">Nome</label>
		<input type="text" name="name" value="<?php echo escape($user->data()->name); ?>">
		
		<input type="submit" value="Atualizar">
		<input type="hidden" name="token" value="<?php echo Token::generate(); ?>">
	</div>
</form>