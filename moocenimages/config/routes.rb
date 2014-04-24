Moocenimages::Application.routes.draw do
  # admin routes
  get "admin/users"
  get "admin/visualizations"
  get "admin/offerings"
  put "admin/approve_user/:user_id"  => "admin#approve_user", :as => :approve_user

  devise_for :users
  root :to => "visualizations#index"

  resources :visualizations, :only => [:index, :new, :create, :show]
  resources :offerings, :only => [:new, :create]

  get 'about' => 'home#about'
  post 'get_upload' => 'visualizations#get_upload'
  post 'get_path_to_public_data' => 'visualizations#get_path_to_public_data'
  get 'get_zip' => 'visualizations#get_zip'

  get '/new_viz_step_2' => 'visualizations#new_step_2'
  post '/create_viz_step_2' => 'visualizations#create_step_2'

  get '/new_viz_step_3' => 'visualizations#new_step_3'
  post '/create_viz_step_3' => 'visualizations#create_step_3'

  get '/new_viz_step_4' => 'visualizations#new_step_4'
  post '/create_viz_step_4' => 'visualizations#create_step_4'

  get '/new_viz_step_5' => 'visualizations#new_step_5'
  post '/create_viz_step_5' => 'visualizations#create_step_5'

  get '/new_viz_step_6' => 'visualizations#new_step_6'
  post '/create_viz_step_6' => 'visualizations#create_step_6'
end
