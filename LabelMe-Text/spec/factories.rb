FactoryGirl.define do
  factory :user do
    sequence(:name) { |n| "Person #{n}" }
    sequence(:email) { |n| "person_#{n}@example.com" }
    password "foobar"
    password_confirmation "foobar"

    factory :admin do
      admin true
    end
  end

  factory :post do
    content "Here's a post"
    user
  end

  factory :sentence do
    content "Here's a post."
    post
  end

  factory :response do
    user
    sentence
    label "content"
  end
end
