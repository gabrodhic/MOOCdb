Moocenimages::Application.routes.draw do
  get "gallery" => 'gallery#index'
  root :to => "visualizations#index"


  resources :users
  resources :user_sessions
end
