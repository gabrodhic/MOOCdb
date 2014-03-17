Moocenimages::Application.routes.draw do
  devise_for :users
  root :to => "visualizations#index"

  resources :visualizations
  resources :uploads

  get 'login' => 'user_sessions#new', :as => :login
  get 'logout' => 'user_sessions#destroy', :as => :logout
  get 'about' => 'visualizations#about'
  post 'get_upload' => 'visualizations#get_upload'
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
