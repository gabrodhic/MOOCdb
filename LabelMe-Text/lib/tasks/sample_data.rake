namespace :db do
  desc "Fill database with sample data"
  task populate: :environment do
    User.create!(name: "Example User",
                 email: "example@railstutorial.org",
                 password: "foobar",
                 password_confirmation: "foobar",
                 admin: true)
    User.create!(name: "Chuck Testa",
                 email: "nope@chucktesta.com",
                 password: "foobar",
                 password_confirmation: "foobar",
                 admin: true)    
  end
end                
