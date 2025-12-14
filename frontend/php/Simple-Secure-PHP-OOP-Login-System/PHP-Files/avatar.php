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
			'avatar' => array(
				'required' => true,
				'min' => 10,
				'max' => 150
			)
		));
		
		if($validation->passed()){
			$extension = substr($_POST['avatar'], -3);
			
			if($extension == "png" || $extension == "jpg" || $extension == "jpeg"){
				$external_link = $_POST['avatar'];
				if (@getimagesize($external_link)) {
					try{
						$user->update(array(
							'avatar' => Input::get('avatar')
						));
						
						Session::flash('home', 'Seu avatar foi atualizado.');
						Redirect::to('index.php');
						
					}catch(Exception $e){
						die($e->getMessage());
					}
				} else {
					echo  "Imagem inexistente no endereço informado.";
				}
					
			}else{
				echo "Extensão incorreta, certifique-se de que o link é uma imagem terminada em .png, .jpg ou .jpeg";
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
		<label for="avatar">URL</label>
		<input type="text" name="avatar" value="<?php echo escape($user->data()->avatar); ?>">
		
		<input type="submit" value="Atualizar">
		<input type="hidden" name="token" value="<?php echo Token::generate(); ?>">
	</div>
</form>