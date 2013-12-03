Moocenimages::Application.routes.draw do
  get "gallery" => 'gallery#index'
  root :to => "visualizations#index"


  resources :users
  resources :user_sessions

  get 'login' => 'user_sessions#new', :as => :login
  get 'logout' => 'user_sessions#destroy', :as => :logout
end
