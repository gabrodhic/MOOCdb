Moocenimages::Application.routes.draw do
  root :to => "visualizations#index"

  resources :users
  resources :user_sessions
  resources :visualizations
  resources :uploads

  get 'login' => 'user_sessions#new', :as => :login
  get 'logout' => 'user_sessions#destroy', :as => :logout
  post 'get_upload' => 'visualizations#get_upload'
end
