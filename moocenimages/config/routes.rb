Moocenimages::Application.routes.draw do
  root :to => "visualizations#index"

  resources :users
  resources :user_sessions

  get 'login' => 'user_sessions#new', :as => :login
  get 'logout' => 'user_sessions#destroy', :as => :logout

end
